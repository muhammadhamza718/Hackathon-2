# Implementation Tasks: Premium Visual Todo TUI (Phase-1)

**Feature**: Premium Visual Todo TUI (Phase-1)
**Branch**: `001-premium-tui`
**Created**: 2026-01-06
**Input**: Feature specification from `/specs/001-premium-tui/spec.md`

## Implementation Strategy

Implement the Premium Visual Todo TUI following the "Visuals First, Functionality Second" philosophy. Focus on creating the visual aesthetic first (gradient ASCII logo, themed components) before implementing core functionality. Each user story will be implemented as an independently testable increment.

### MVP Scope
The MVP will include User Story 1 (Launch Premium TUI) with basic visual elements and User Story 2 (Add Task via Modal) for core functionality, providing a complete but minimal working application.

## Phase 1: Setup

### Goal
Initialize project dependencies and create necessary directory structure for the premium TUI implementation.

- [ ] T001 Add `textual` and `rich` dependencies to pyproject.toml
- [ ] T002 Create `src/ui/assets.py` to hold the ASCII Art for the "TODO" logo
- [ ] T003 Define the Color Palette (Gradient: Cyan -> Purple) in a theme config
- [ ] T004 Create directory `src/ui/components/` for modal components
- [ ] T005 Create `src/ui/premium_todo_app.py` as the main Textual application file

## Phase 2: Foundational

### Goal
Implement foundational components that all user stories depend on, including data model verification and service enhancements.

- [ ] T006 Verify `Task` model has ONLY: `id`, `title`, `description`, `completed`, `created_at` in `src/models/task.py`
- [ ] T007 Remove Priority functionality from `src/models/task.py` and `src/models/priority.py` (Phase-1 scope)
- [ ] T008 Implement `search_tasks` method in `TaskService` in `src/services/task_service.py`
- [ ] T009 Implement `filter_tasks` (by status only) in `TaskService` in `src/services/task_service.py`
- [ ] T010 Create base Textual application structure in `src/ui/premium_todo_app.py`

## Phase 3: User Story 1 - Launch Premium TUI (Priority: P1)

### Goal
User launches the application and is greeted with a visually premium terminal user interface featuring a large gradient ASCII art logo that displays "TODO" in cyan-to-purple gradient.

### Independent Test
The application can be launched and the user can see the large gradient "TODO" logo immediately upon startup, delivering the premium visual experience as the first interaction.

- [ ] T011 [US1] Implement `Header` widget using `rich.text.Text` to render the Gradient ASCII Logo in `src/ui/premium_todo_app.py`
- [ ] T012 [US1] Create ASCII art generator function in `src/ui/assets.py` for "TODO" text
- [ ] T013 [US1] Apply gradient styling (Cyan -> Purple) to the "TODO" logo using Rich
- [ ] T014 [US1] Implement theme configuration with specified hex codes: Background (#0f0f14), Foreground (#e0e0e0), Accents (#00bfff, #bf0f0ff) in `src/ui/premium_todo_app.py`
- [ ] T015 [US1] Build the Main Layout (Sidebar + Header + Content) in `src/ui/premium_todo_app.py`
- [ ] T016 [US1] Implement the Sidebar with simple filters: `All`, `Pending`, `Completed` in `src/ui/premium_todo_app.py`
- [ ] T017 [US1] Test application launch with visual elements

## Phase 4: User Story 2 - Add Task via Modal (Priority: P1)

### Goal
User can add new tasks by pressing 'a' key, which opens a modal dialog allowing entry of task title and description, with the input fields styled appropriately to match the premium visual theme.

### Independent Test
User can press 'a', see a modal dialog, enter title and description, and have the task added to the list, providing the core task creation functionality.

- [ ] T018 [US2] Create `AddTaskModal` class in `src/ui/components/add_task_modal.py`
- [ ] T019 [US2] Implement styled input fields in `AddTaskModal` with premium visual theme
- [ ] T020 [US2] Add validation for title (max 50 chars) and description (max 200 chars) in `AddTaskModal`
- [ ] T021 [US2] Implement keyboard shortcut 'a' to open `AddTaskModal` in `src/ui/premium_todo_app.py`
- [ ] T022 [US2] Connect `AddTaskModal` to `TaskService` for task creation
- [ ] T023 [US2] Update task list display after adding a new task
- [ ] T024 [US2] Test task creation via modal dialog

## Phase 5: User Story 3 - View Tasks with Visual Status Indicators (Priority: P1)

### Goal
User can view all tasks in a DataTable with custom visual indicators for status (completed/pending) using appropriate icons (✅ for completed, ⏳ for pending), with proper visual styling matching the theme.

### Independent Test
User can see all tasks listed with appropriate status icons and visual styling, providing clear visual feedback about task completion status.

- [ ] T025 [US3] Customize `DataTable` to use Unicode icons (✅, ⏳) for the Status column in `src/ui/premium_todo_app.py`
- [ ] T026 [US3] Create custom cell renderer for status indicators in `src/ui/premium_todo_app.py`
- [ ] T027 [US3] Implement DataTable with columns: ID, Status, Title in `src/ui/premium_todo_app.py`
- [ ] T028 [US3] Connect DataTable to TaskService to display all tasks
- [ ] T029 [US3] Implement proper styling for DataTable to match theme
- [ ] T030 [US3] Add scrolling capability to DataTable for many tasks
- [ ] T031 [US3] Test task display with visual status indicators

## Phase 6: User Story 4 - Task Management Actions (Priority: P2)

### Goal
User can perform all core task management operations (Update, Delete, Toggle Complete) using keyboard shortcuts, with visual feedback and proper error handling.

### Independent Test
User can perform each operation (update, delete, toggle complete) using keyboard shortcuts and see the results reflected in the interface.

- [ ] T032 [US4] Implement keyboard shortcut 'u' for update task in `src/ui/premium_todo_app.py`
- [ ] T033 [US4] Create `EditTaskModal` class in `src/ui/components/edit_task_modal.py`
- [ ] T034 [US4] Implement keyboard shortcut 'd' for delete task with confirmation in `src/ui/premium_todo_app.py`
- [ ] T035 [US4] Implement keyboard shortcut 'c' for toggle completion in `src/ui/premium_todo_app.py`
- [ ] T036 [US4] Connect update functionality to `EditTaskModal` and TaskService
- [ ] T037 [US4] Connect delete functionality to TaskService with confirmation dialog
- [ ] T038 [US4] Connect toggle completion functionality to TaskService
- [ ] T039 [US4] Update UI after each operation to reflect changes
- [ ] T040 [US4] Test all task management operations via keyboard shortcuts

## Phase 7: User Story 5 - Search and Filter Tasks (Priority: P2)

### Goal
User can focus the search bar by pressing '/' key and filter tasks by title, with real-time filtering of the task list as they type.

### Independent Test
User can press '/' to focus search, type query text, and see the task list filter in real-time based on title matches.

- [ ] T041 [US5] Create a styled `SearchInput` widget with a custom border and prompt in `src/ui/premium_todo_app.py`
- [ ] T042 [US5] Implement keyboard shortcut '/' to focus search input in `src/ui/premium_todo_app.py`
- [ ] T043 [US5] Connect search input to TaskService `search_tasks` method
- [ ] T044 [US5] Implement real-time filtering as user types in search field
- [ ] T045 [US5] Update DataTable display based on search results
- [ ] T046 [US5] Clear search functionality to reset to all tasks
- [ ] T047 [US5] Test search and filter functionality

## Phase 8: Polish & Cross-Cutting Concerns

### Goal
Final implementation touches, error handling, and integration of all components.

- [ ] T048 Implement graceful exit when 'q' key is pressed in `src/ui/premium_todo_app.py`
- [ ] T049 Add proper error handling for all operations with user-friendly messages
- [ ] T050 Handle edge case: What happens when user tries to add a task with an empty title
- [ ] T051 Handle edge case: How system handles invalid keyboard input
- [ ] T052 Handle edge case: What happens when user tries to delete a task that doesn't exist
- [ ] T053 Handle edge case: How system handles very long task titles or descriptions (truncate appropriately in display)
- [ ] T054 Implement proper input validation throughout the application
- [ ] T055 Test complete user flow: add → view → update → complete → delete
- [ ] T056 Update main.py to launch the premium TUI by default
- [ ] T057 Conduct final integration testing of all components

## Dependencies

### User Story Completion Order
1. **User Story 1** (Launch Premium TUI) - Foundation for all other stories
2. **User Story 3** (View Tasks) - Depends on User Story 1
3. **User Story 2** (Add Task) - Depends on User Story 1 and 3
4. **User Story 4** (Task Management) - Depends on User Story 2 and 3
5. **User Story 5** (Search and Filter) - Depends on User Story 3

### Parallel Execution Examples

**User Story 1 Parallel Tasks:**
- T011 [P] [US1] Implement Header widget
- T012 [P] [US1] Create ASCII art generator
- T013 [P] [US1] Apply gradient styling
- T014 [P] [US1] Implement theme configuration

**User Story 2 Parallel Tasks:**
- T018 [P] [US2] Create AddTaskModal class
- T019 [P] [US2] Implement styled input fields
- T020 [P] [US2] Add validation logic

## Testing Strategy

- Each user story should be independently testable
- Unit tests for service layer functionality
- Component tests for Textual UI elements
- Integration tests for complete workflows
- Cross-platform compatibility verification