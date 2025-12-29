---
description: "Task list for Admin Dashboard Refinements feature implementation"
---

# Tasks: Admin Dashboard Refinements

**Input**: Design documents from `/specs/007-admin-ui-refinements/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)
**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Frontend**: `frontend/app/`
- **Backend**: `backend/api/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Define Admin API endpoints structure in backend/api/admin.py
- [x] T002 Update frontend API client definition in frontend/lib/api.ts

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T003 Implement backend `adminDeleteUser` logic in backend/api/admin.py
- [x] T004 Implement backend `update_user_role` logic in backend/api/admin.py
- [x] T005 Implement backend `delete_user_task` logic in backend/api/admin.py
- [x] T006 Expose `adminDeleteUser`, `adminUpdateUserRole`, `adminDeleteTask` in frontend/lib/api.ts

**Checkpoint**: Foundation ready - API layers are connected.

---

## Phase 3: User Story 1 - Admin User Management (Priority: P1) 🎯 MVP

**Goal**: Admins can manage users directly from the dashboard.

**Independent Test**: Login as admin -> View User list -> Click "Change Role" or "Delete" -> Verify change.

### Implementation for User Story 1

- [x] T007 [US1] Update `AdminUserCard` to use standard terminology (User/Task) in frontend/components/ui/admin-user-card.tsx
- [x] T008 [US1] Rename "Revoke Access" to "Deactivate" and "Purge" to "Delete" in frontend/components/ui/admin-user-card.tsx
- [x] T009 [US1] Connect Delete User button to `adminDeleteUser` API in frontend/app/admin/dashboard/page.tsx
- [x] T010 [US1] Connect Change Role button to `adminUpdateUserRole` API in frontend/app/admin/dashboard/page.tsx
- [x] T011 [US1] Implement confirmation modal for user deletion in frontend/components/admin/confirmation-modal.tsx

**Checkpoint**: At this point, User Story 1 is fully functional.

---

## Phase 4: User Story 2 - Admin Task Oversight (Priority: P1)

**Goal**: Admins can oversee and moderate user tasks.

**Independent Test**: Login as admin -> Select User -> View Tasks stream -> Delete a task -> Verify removal.

### Implementation for User Story 2

- [x] T012 [US2] Implement task fetching logic for users in backend/api/admin.py
- [x] T013 [US2] Display task stream in admin user card view in frontend/app/admin/dashboard/page.tsx
- [x] T014 [US2] Connect Delete Task button to `adminDeleteTask` API in frontend/app/admin/dashboard/page.tsx
- [x] T015 [US2] Handle empty states ("No active logs" -> "No tasks found") in frontend/app/admin/dashboard/page.tsx

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently.

---

## Phase 5: User Story 3 - Task Creation & Interface (Priority: P2)

**Goal**: Standard users can easily create tasks with a clear UI.

**Independent Test**: Login as user -> Click "New Task" -> Verify modal clarity -> Create task.

### Implementation for User Story 3

- [x] T016 [US3] Create `CreateTaskDialog` component with accessible UI in frontend/components/create-task-dialog.tsx
- [x] T017 [US3] Ensure modal uses solid white background and dark text for contrast in frontend/components/create-task-dialog.tsx
- [x] T018 [US3] Integrate CreateTaskDialog into main dashboard in frontend/app/(app)/dashboard/page.tsx
- [x] T019 [US3] Implement optimistic UI updates for task list upon creation in frontend/app/(app)/dashboard/page.tsx

**Checkpoint**: All user stories are now independently functional.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T020 Fix Sidebar navigation links in frontend/components/admin/sidebar.tsx
- [x] T021 Add "Admin" link to main navigation for admin users in frontend/components/navigation.tsx
- [x] T022 Remove all "spy" jargon from Dashboard headers and labels in frontend/app/admin/dashboard/page.tsx

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Completed first to define API contracts.
- **Foundational (Phase 2)**: Completed to enable backend logic.
- **User Stories (Phase 3+)**: Implemented sequentially (User Mgmt -> Task Oversight -> UI Polish).
- **Polish (Final Phase)**: Completed to clean up jargon and navigation.

### Implementation Strategy

### MVP First (User Story 1 Only)

1. Completed Phase 1 & 2 (API Layer)
2. Completed Phase 3 (User Management UI)

### Incremental Delivery

1. Added Task Oversight (Phase 4)
2. Added UI Refinements (Phase 5 & 6)
