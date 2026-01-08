# Feature Specification: Premium Visual Todo TUI (Phase-1)

**Feature Branch**: `001-premium-tui`
**Created**: 2026-01-06
**Status**: Draft
**Input**: User description: "Create a detailed technical specification for the Premium Visual Todo TUI (Phase-1).
The specification should focus heavily on the Visual Layer while keeping the Logic Layer minimal.
1.  **Visual Specification (The \"Gemini\" Look)**:
    *   **Header Component**: Must define a \"Big Text\" rendering logic using `rich` or `pyfiglet` to display \"TODO\" in a gradient (Cyan -> Purple).
    *   **Main List**: `Textual` DataTable with custom cell renderers for status icons (e.g., `✅`, `⏳`).
    *   **Input Area**: A stylized `Input` widget with a colored border and prompt string (e.g., `> `).
    *   **Theme**: Define specific hex codes for Background (`#0f0f14`), Foreground (`#e0e0e0`), and Accents (`#00bfff`, `#bf00ff`).
2.  **Functional Specification (Strict Phase-1)**:
    *   **Actions**: Add, List, Update, Delete, Toggle Complete.
    *   **Data Model**:
        *   `Task(id: int, title: str, description: str, completed: bool, created_at: datetime)`
        *   *Explicitly exclude* Priority and Tags.
3.  **User Scenarios**:
    *   User launches app -> Sees big \"TODO\" logo.
    *   User presses `a` -> Modal dialog appears for Title/Description.
    *   User types `/` -> Focuses search bar (filtering by title only).
    *   User presses `q` -> App exits gracefully.
Reflecting the updated plan: @C:\Users\HP\.gemini\antigravity\brain\26fcafb8-fdb1-48cb-ba9a-278958727569\implementation_p"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Launch Premium TUI (Priority: P1)

User launches the application and is greeted with a visually premium terminal user interface featuring a large gradient ASCII art logo that displays "TODO" in cyan-to-purple gradient, immediately conveying the "gemini-cli" aesthetic.

**Why this priority**: This is the foundational user experience that sets the premium visual tone and differentiates the application from standard CLI interfaces. Without this core visual element, the premium nature of the application cannot be established.

**Independent Test**: The application can be launched and the user can see the large gradient "TODO" logo immediately upon startup, delivering the premium visual experience as the first interaction.

**Acceptance Scenarios**:

1. **Given** user runs the application, **When** application starts, **Then** a large gradient ASCII art "TODO" logo appears at the top of the interface in cyan-to-purple gradient
2. **Given** application is running, **When** user sees the interface, **Then** the visual theme matches gemini-cli aesthetic with deep background (#0f0f14) and bright accent colors

---

### User Story 2 - Add Task via Modal (Priority: P1)

User can add new tasks by pressing 'a' key, which opens a modal dialog allowing entry of task title and description, with the input fields styled appropriately to match the premium visual theme.

**Why this priority**: Core functionality to create tasks is essential for the todo application's primary purpose, and the modal approach provides a clean user experience that fits the TUI aesthetic.

**Independent Test**: User can press 'a', see a modal dialog, enter title and description, and have the task added to the list, providing the core task creation functionality.

**Acceptance Scenarios**:

1. **Given** application is running with task list displayed, **When** user presses 'a' key, **Then** a modal dialog appears with fields for title and description
2. **Given** modal dialog is open, **When** user enters valid title and description and confirms, **Then** new task appears in the task list with pending status
3. **Given** modal dialog is open, **When** user enters invalid input (title > 50 chars), **Then** appropriate validation error is shown

---

### User Story 3 - View Tasks with Visual Status Indicators (Priority: P1)

User can view all tasks in a DataTable with custom visual indicators for status (completed/pending) using appropriate icons (✅ for completed, ⏳ for pending), with proper visual styling matching the theme.

**Why this priority**: This provides the core task viewing functionality with visual enhancements that align with the premium aesthetic goals.

**Independent Test**: User can see all tasks listed with appropriate status icons and visual styling, providing clear visual feedback about task completion status.

**Acceptance Scenarios**:

1. **Given** application has tasks, **When** user views the main screen, **Then** all tasks are displayed in a DataTable with ID, Title, and Status columns
2. **Given** tasks exist in the system, **When** user views the task list, **Then** completed tasks show ✅ icon and pending tasks show ⏳ icon
3. **Given** user has many tasks, **When** viewing the list, **Then** the table is scrollable to see all tasks

---

### User Story 4 - Task Management Actions (Priority: P2)

User can perform all core task management operations (Update, Delete, Toggle Complete) using keyboard shortcuts, with visual feedback and proper error handling.

**Why this priority**: These operations complete the core CRUD functionality needed for task management while maintaining the keyboard-driven TUI experience.

**Independent Test**: User can perform each operation (update, delete, toggle complete) using keyboard shortcuts and see the results reflected in the interface.

**Acceptance Scenarios**:

1. **Given** tasks exist in the list, **When** user presses 'u' key, **Then** update modal appears with current task data pre-filled
2. **Given** user has selected a task, **When** user presses 'd' key, **Then** delete confirmation appears and task is removed if confirmed
3. **Given** user has selected a task, **When** user presses 'c' key, **Then** task completion status toggles and visual indicator updates

---

### User Story 5 - Search and Filter Tasks (Priority: P2)

User can focus the search bar by pressing '/' key and filter tasks by title, with real-time filtering of the task list as they type.

**Why this priority**: Search functionality enhances usability for users with many tasks, providing quick access to specific tasks.

**Independent Test**: User can press '/' to focus search, type query text, and see the task list filter in real-time based on title matches.

**Acceptance Scenarios**:

1. **Given** application is running with tasks, **When** user presses '/' key, **Then** search input field receives focus
2. **Given** search field is focused, **When** user types text, **Then** task list updates to show only tasks with matching titles
3. **Given** search filter is active, **When** user clears the search, **Then** all tasks are displayed again

---

### Edge Cases

- What happens when user tries to add a task with an empty title? (Should show validation error)
- How does system handle invalid keyboard input? (Should be gracefully ignored)
- What happens when user tries to delete a task that doesn't exist? (Should show appropriate error message)
- How does system handle very long task titles or descriptions? (Should truncate appropriately in the display)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST display a large gradient ASCII art "TODO" logo in the header using cyan-to-purple gradient
- **FR-002**: System MUST provide keyboard shortcuts for all core operations (a=add, u=update, d=delete, c=toggle complete, q=quit)
- **FR-003**: System MUST allow users to add tasks with title (required, max 50 chars) and description (optional, max 200 chars)
- **FR-004**: System MUST display tasks in a DataTable with columns: ID, Status, Title
- **FR-005**: System MUST use visual indicators (✅, ⏳) to show task completion status
- **FR-006**: System MUST allow users to update existing tasks
- **FR-007**: System MUST allow users to delete tasks with confirmation
- **FR-008**: System MUST allow users to toggle task completion status
- **FR-009**: System MUST provide search functionality that filters tasks by title only
- **FR-010**: System MUST follow the specified theme with background (#0f0f14), foreground (#e0e0e0), and accent colors (#00bfff, #bf00ff)
- **FR-011**: System MUST NOT include Priority or Tags functionality (strict Phase-1 scope)
- **FR-012**: System MUST use modal dialogs for task creation and updates
- **FR-013**: System MUST provide graceful exit when 'q' key is pressed

### Key Entities *(include if feature involves data)*

- **Task**: Represents a single todo item with id (int), title (str), description (str), completed (bool), and created_at (datetime). This entity forms the core data model for the application.
- **TaskList**: Collection of Task entities that can be filtered, searched, and displayed in the DataTable interface.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can see the premium "gemini-cli" aesthetic with the gradient "TODO" logo within 1 second of application launch
- **SC-002**: Users can add, view, update, delete, and toggle task completion with keyboard shortcuts in under 5 seconds each
- **SC-003**: Users can search and filter tasks by title with results updating in real-time (under 0.5 seconds response time)
- **SC-004**: 95% of users successfully complete the primary task flow (add → view → update → complete → delete) on first attempt
- **SC-005**: Application maintains visual consistency with specified theme colors across all interface elements
