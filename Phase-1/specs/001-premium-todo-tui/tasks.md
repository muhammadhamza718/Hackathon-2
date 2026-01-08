# Testable Tasks: Premium Todo TUI (Phase-1)

**Feature**: `001-premium-todo-tui`
**Branch**: `001-premium-todo-tui`
**Created**: 2026-01-06
**Status**: Draft
**Author**: Claude Sonnet 4.5

## Implementation Strategy

*How will we deliver this feature incrementally?*

- MVP: Basic TUI with task creation and display using Textual
- Iteration 2: Add search and filtering capabilities
- Final: Complete TUI with all keyboard shortcuts, visual indicators, and polish

## Dependencies

*What must be completed before each user story?*

- All user stories depend on Phase 1 (Setup) and Phase 2 (Foundational) being completed
- User Story 4 (Keyboard shortcuts) depends on basic UI components from other stories being available
- User Story 5 (Visual indicators) depends on the task display component from other stories

## Parallel Execution Examples

*How can we work on tasks simultaneously?*

- T001-T005 (Setup tasks) can be done in parallel with each other
- T006-T010 (Foundational tasks) can be developed in parallel with proper interface definitions
- US1 and US4 (Add Task and Keyboard shortcuts) can be developed in parallel after foundational tasks
- UI components (Task List, Sidebar, Search Bar) can be developed in parallel after foundational tasks

## Phase 1: Setup

*Project initialization and foundational setup*

- [x] T001 Update pyproject.toml to include textual and rich dependencies
- [x] T002 Create project directory structure (src/, tests/, docs/)
- [x] T003 [P] Set up basic main.py file with placeholder for TUI app
- [x] T004 [P] Create Task model with ID, Title, Description, Priority, Completed, Tags, CreatedAt
- [x] T005 [P] Create Priority Enum with Low, Medium, High values

## Phase 2: Foundational

*Blocking prerequisites for all user stories*

- [x] T006 Create TaskStorage class with in-memory storage for tasks
- [x] T007 Create TaskService with add_task, update_task, delete_task, toggle_task_completion methods
- [x] T008 Implement search functionality in TaskService (search_tasks method)
- [x] T009 Implement filtering functionality in TaskService (filter_tasks method)
- [x] T010 Add input validation to TaskService (title max 50 chars, description max 200 chars)

## Phase 3: Add Task with Priority and Tags (Priority: P1)

*Goal: User can add new tasks with title, description, priority, and tags*

**Independent Test**: User can open the add task dialog, enter all required fields, and see the new task appear in the task list with correct properties.

- [x] T011 [US1] Create AddTaskModal component with fields for title, description, priority, and tags
- [x] T012 [US1] Implement validation in AddTaskModal (title required, max 50 chars)
- [x] T013 [US1] Connect AddTaskModal to TaskService to create new tasks
- [x] T014 [US1] Add keyboard shortcut 'A' to open AddTaskModal
- [x] T015 [US1] Verify new task appears in task list with correct properties after creation

## Phase 4: Manage Tasks with Keyboard Shortcuts (Priority: P1)

*Goal: User can perform all CRUD operations using keyboard shortcuts*

**Independent Test**: User can perform all core operations (add, delete, update, toggle complete) using keyboard shortcuts.

- [x] T016 [US4] Implement keyboard shortcut 'D' to delete selected task
- [x] T017 [US4] Implement keyboard shortcut 'C' to toggle completion status
- [x] T018 [US4] Implement keyboard shortcut 'U' to open update task modal
- [x] T019 [US4] Create EditTaskModal component pre-filled with selected task data
- [x] T020 [US4] Connect keyboard shortcuts to TaskService operations

## Phase 5: Search Tasks in Real-time (Priority: P2)

*Goal: User can search through tasks in real-time*

**Independent Test**: User can type in a search bar and see the task list filter in real-time as they type.

- [x] T021 [US2] Create SearchBarComponent with real-time filtering capability
- [x] T022 [US2] Connect SearchBarComponent to TaskService search functionality
- [x] T023 [US2] Implement keyboard shortcut '/' to focus search bar
- [x] T024 [US2] Ensure search updates task list immediately as user types
- [x] T025 [US2] Add clear search functionality when search is cleared

## Phase 6: Filter Tasks by Status and Priority (Priority: P2)

*Goal: User can filter tasks by status and priority*

**Independent Test**: User can select different filter options and see the task list update accordingly.

- [x] T026 [US3] Create SidebarComponent with filter navigation options
- [x] T027 [US3] Implement status filters (All, Pending, Completed) in sidebar
- [x] T028 [US3] Implement priority filters (All, Low, Medium, High) in sidebar
- [x] T029 [US3] Connect filters to TaskService filtering functionality
- [x] T030 [US3] Add keyboard shortcut 'F' to focus filter sidebar

## Phase 7: View Tasks with Visual Priority Indicators (Priority: P2)

*Goal: Tasks display with clear visual indicators for priorities*

**Independent Test**: User can visually distinguish between different priority levels through color coding and icons.

- [x] T031 [US5] Create TaskListComponent using Textual DataTable
- [x] T032 [US5] Implement custom cell rendering for priority indicators
- [x] T033 [US5] Add color coding for priority levels (Red for High, Yellow for Medium, Green for Low)
- [x] T034 [US5] Add icons for priority levels and completion status
- [x] T035 [US5] Ensure visual indicators work for color-blind users with symbols

## Phase 8: TUI Foundation

*Goal: Create the main application structure with Header, Sidebar, Main, and Footer*

**Independent Test**: The application displays with proper layout structure and all components are accessible.

- [x] T036 Create PremiumTodoApp class inheriting from Textual App
- [x] T037 Implement HeaderComponent with application title and status stats
- [x] T038 Implement FooterComponent with keyboard shortcut hints
- [x] T039 Implement main layout with Header, Sidebar, Main Content, and Footer
- [x] T040 Update main.py to launch the PremiumTodoApp

## Phase 9: Polish & Cross-Cutting

*Final integration, testing, and refinement*

- [x] T041 Add responsive design for window resizing
- [x] T042 Implement proper error handling and user feedback
- [x] T043 Add loading states for UI operations
- [x] T044 Implement proper exit handling (keyboard shortcut 'Q')
- [x] T045 Add visual polish and ensure consistent styling across components

## Validation

*How do we know this is complete?*

- [x] All user stories (US1-US5) are independently testable and functional
- [x] All keyboard shortcuts work as specified in quickstart guide
- [x] Search and filtering work in real-time as specified
- [x] Visual indicators for priorities are clear and distinguishable
- [x] All validation rules are enforced (title max 50 chars, description max 200 chars)
- [x] Application is responsive during window resizing
- [x] All acceptance scenarios from the spec are satisfied