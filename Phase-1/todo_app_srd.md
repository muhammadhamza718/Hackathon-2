# HydroToDo - Phase I: In-Memory Console Application Specification

## 1. Executive Summary

**HydroToDo (Phase I)** is a high-performance, terminal-based task management application. It fulfills the **Phase 1** requirements of the _Hackathon II_ specification (In-Memory, Basic CRUD) while delivering a premium **UI/UX** inspired by professional TUI tools.

This specification mandates a **Curses-based interface** with tabbed navigation and split-pane viewing, strictly operating **in-memory** during execution, with optional JSON state preservation.

## 2. Project Constraints & Scope

- **Hackathon Phase:** Phase I (In-Memory Console App).
- **Core Goal:** Master Spec-Driven Development using standard libraries.
- **Platform:** Console/Terminal (Cross-platform).
- **Dependencies:** Standard Library ONLY (`curses`, `json`, `textwrap`, `datetime`). **No external packages.**

## 3. User Interface (UI) Specification

The User Interface must strictly replicate the "HydroToDo" design provided in the reference implementation.

### 3.1 Layout Architecture

The screen is composed of 4 vertical sections:

```text
Section 1: HEADER
┌─────────────────────────────────────────────────────────────┐
│  ASCII ART TITLE ("HydroToDo" or similar)                   │
└─────────────────────────────────────────────────────────────┘

Section 2: NAVIGATION BAR
   [ GENERAL ]   WORK    PERSONAL    (Tabs)

Section 3: MAIN CONTENT SPLIT-VIEW
┌─ Task List (Left) ───────────┐ ┌─ Detail Pane (Right) ──────┐
│ [X] Task One (Done)          │ │ TASK: Task One             │
│ [ ] Task Two (Pending)       │ │                            │
│ [ ] Task Three               │ │ CREATED: 2026-02-03        │
│                              │ │                            │
│                              │ │ NOTES:                     │
│                              │ │ Detailed notes content     │
│                              │ │ goes here...               │
└──────────────────────────────┘ └────────────────────────────┘

Section 4: FOOTER / STATUS
   [H]elp  [A]dd  [D]elete  [N]otes  [Q]uit
```

### 3.2 Visual Style

- **Colors:** Use standard terminal colors.
  - **Active Tab/Selection:** Reverse Video (White on Black).
  - **Borders:** Standard or Dimmed.
  - **Success:** Green (for `[X]` status).
- **Typography:**
  - Standard Monospace.
  - Box-drawing characters (`┌`, `─`, `┐`, `│`, `└`, `┘`) for all borders.

### 3.3 Interactive Components

- **Tab System:** Allows categorizing tasks. Even for Phase 1, basic categorization (General, Work, etc.) is supported to enable the UI layout.
- **Input Overlay:** Modal text input at the bottom of the screen for adding tasks.
- **Multi-line Editor:** A basic modal editor for "Notes" field.

## 4. Functional Requirements (Phase 1 Aligned)

### 4.1 Data Storage (In-Memory)

- **FR-01:** The application must store all data in **Python Data Structures** (Lists/Dictionaries) during runtime.
- **FR-02:** No database (SQLite/PostgreSQL) is strictly required for Phase 1 logic, aligning with the "In-Memory" constraint.
- **FR-03:** _Persistence:_ To make the tool usable, data should be serialized to a JSON file (`todo_data.json`) on exit and loaded on startup.

### 4.2 Core Features (CRUD)

The app implements the 5 Basic Level features required by Phase 1:

| Req ID    | Feature           | Description        | UI Action                            |
| :-------- | :---------------- | :----------------- | :----------------------------------- |
| **FR-04** | **Add Task**      | Create a new item. | Press `a` -> Input prompt appears.   |
| **FR-05** | **View List**     | See all tasks.     | Main View (Left Pane).               |
| **FR-06** | **Update Task**   | Edit details.      | Press `n` to edit Notes/Description. |
| **FR-07** | **Delete Task**   | Remove item.       | Press `d` on selected item.          |
| **FR-08** | **Mark Complete** | Toggle status.     | Press `Enter` on selected item.      |

### 4.3 Navigation & Controls

The keybindings must match the HydroToDo reference:

- `k` / `Up Arrow`: Move cursor Up.
- `j` / `Down Arrow`: Move cursor Down.
- `h` / `Left Arrow`: Previous Tab.
- `l` / `Right Arrow`: Next Tab.
- `Enter`: Toggle Completion Status.
- `a`: Add New Task.
- `d`: Delete Selected Task.
- `n`: Edit Task Notes (Update).
- `Alt+p`: Toggle Preview Pane.
- `q`: Quit Application.

## 5. Technical Implementation Guidelines

### 5.1 Python Structure

```python
class Task:
    id: int
    title: str
    done: bool
    category: str
    created_at: str
    notes: str

class TodoApp:
    tasks: List[Task]
    current_tab: str
    # Methods: load_data(), save_data(), add_task(), etc.
```

### 5.2 Curses View Logic

- Use `curses.wrapper` to handle initialization.
- Use `stdscr.getch()` in a `while True` loop for event handling.
- Implement a custom `wrap_text` utility for the Note display to ensure text fits within the Preview Pane.

## 6. Deliverables

- `src/todo_app.py`: Complete source code.
- `README.md`: Setup and usage instructions.
