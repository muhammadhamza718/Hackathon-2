---
id: 2
title: update-phase1-constitution
stage: constitution
date: 2026-01-06
surface: agent
model: Claude Sonnet 4.5
feature: none
branch: 001-phase-5-advanced-todo
user: user
command: sp.constitution
labels: [constitution, phase1, todo, tui]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
  - .specify/templates/plan-template.md
tests:
  - none
---

## Prompt

```text
Generate a constitution for Phase-1 of the "Evolution of Todo" project.
The core objective is to build a premium Terminal User Interface (TUI) for an in-memory Python console app, inspired by the high-quality interface of Gemini CLI.
Non-Negotiables:
1. UI Framework: Use 'Textual' and 'Rich' for the interface. No simple print/input loops.
2. Aesthetic: The TUI must feel modern, interactive, and "pro", with mouse support, keyboard shortcuts, and a clear layout (Sidebar, Header, Main Content, Footer).
3. Core Features: Implement Add, Delete, Update, View, and Toggle Complete.
4. Detailed Features: Include real-time Search, Filtering by status, and Task Priorities (Low, Medium, High).
5. Architecture: Maintain a clean separation between the TUI (View), TaskService (Logic), and TaskStorage (Data).
6. Quality: All outputs must be beautifully formatted with Rich colors and icons (e.g., ✅ status and priority colors).
7. Validation: Strict input validation for title (required, max 50 chars) and description (optional, max 200 chars).
8. Portability: Ensure it runs within a UV-managed virtual environment on Python 3.13+.
```

## Response snapshot

I've successfully updated the constitution for Phase-1 of the "Evolution of Todo" project. Here's my summary:

## Constitution Update Summary

**Version Bump**: 1.0.0 → 1.1.0 (Minor update - added new principles and requirements)

**Changes Made**:
1. Updated the constitution to reflect the specific requirements for Phase-1 of the "Evolution of Todo" project
2. Added new principles specific to the project:
   - UI Framework Excellence (mandating Textual and Rich frameworks)
   - Architectural Separation (TUI/View, TaskService/Logic, TaskStorage/Data)
   - Rich Formatting Quality (colors, icons, visual presentation)
3. Enhanced existing principles to include the new requirements
4. Updated the plan template to align with the new constitution principles
5. Removed the "Minimal Persistence Risk" principle which was replaced with new requirements

**Files Updated**:
- `.specify/memory/constitution.md` - Updated with new Phase-1 requirements
- `.specify/templates/plan-template.md` - Updated Constitution Check section to align with new principles

**Key Requirements Now Reflected**:
- UI Framework: Use 'Textual' and 'Rich' for the interface exclusively
- Aesthetic: Modern, interactive TUI with mouse support, keyboard shortcuts, clear layout (Sidebar, Header, Main Content, Footer)
- Core Features: Add, Delete, Update, View, Toggle Complete
- Detailed Features: Real-time Search, Filtering by status, Task Priorities (Low, Medium, High)
- Architecture: Clean separation between TUI (View), TaskService (Logic), TaskStorage (Data)
- Quality: Rich colors and icons for premium visual experience
- Validation: Strict input validation (title: required, max 50 chars; description: optional, max 200 chars)
- Portability: UV-managed virtual environment on Python 3.13+

The constitution now properly reflects all the non-negotiable requirements you specified for Phase-1 of the project, ensuring all future development will comply with these principles.

## Outcome

- ✅ Impact: Updated constitution to include Phase-1 requirements for TUI Todo app
- 🧪 Tests: none
- 📁 Files: Updated .specify/memory/constitution.md and .specify/templates/plan-template.md
- 🔁 Next prompts: Next steps would involve creating spec, plan, and tasks based on the new constitution
- 🧠 Reflection: Constitution now properly reflects all non-negotiable requirements for Phase-1

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS - all requirements properly incorporated
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): Create feature specification based on updated constitution