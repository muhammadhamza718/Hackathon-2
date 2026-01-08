# Research: Premium Visual Todo TUI (Phase-1)

## Research Summary

This research document addresses the technical decisions required for implementing the Premium Visual Todo TUI (Phase-1) with a focus on visual aesthetics and the "gemini-cli" look and feel.

## Decision: Gradient ASCII Art Implementation
**Rationale**: To create the required "TODO" logo with cyan-to-purple gradient as specified in the constitution and feature spec. The implementation will use Rich's gradient capabilities combined with ASCII art generation.
**Alternatives considered**:
- pyfiglet + manual colorization (more complex)
- Pre-made ASCII art with hardcoded colors (less flexible)
- Textual's built-in widgets (doesn't provide the required "gemini-cli" aesthetic)

## Decision: Textual DataTable Customization
**Rationale**: Using Textual's DataTable widget with custom cell renderers to display tasks with visual status indicators (✅, ⏳) and proper styling to match the gemini-cli aesthetic.
**Alternatives considered**:
- Custom widget implementation (more complex, reinventing existing functionality)
- Plain text list (doesn't meet visual requirements)
- Static display (doesn't support interactivity)

## Decision: Theme and Styling Approach
**Rationale**: Using Textual's CSS-like styling system with the specified color palette (Background: #0f0f14, Foreground: #e0e0e0, Accents: #00bfff, #bf00ff) to ensure consistent visual theme across all components.
**Alternatives considered**:
- Individual styling per widget (inconsistent, harder to maintain)
- Rich-only styling (doesn't provide full TUI control)
- External theme files (overkill for this scope)

## Decision: Modal Implementation for Task Operations
**Rationale**: Using Textual's Screen and Modal classes to create styled dialogs for task creation and updates that match the premium aesthetic.
**Alternatives considered**:
- Inline editing (clutters main interface)
- Pop-up windows with raw input (doesn't match premium aesthetic)
- Menu-driven interface (doesn't meet visual requirements)

## Decision: Search and Filtering Implementation
**Rationale**: Implementing real-time search functionality that filters tasks by title using the existing TaskService methods, updating the DataTable display in real-time as the user types.
**Alternatives considered**:
- Separate search command (less intuitive)
- Full-text search across all fields (exceeds Phase-1 scope)
- Batch filtering (slower user experience)

## Decision: Keyboard Shortcuts Integration
**Rationale**: Using Textual's binding system to implement keyboard shortcuts (a, u, d, c, q) for core operations to provide efficient keyboard-driven workflow.
**Alternatives considered**:
- Menu-based commands (slower interaction)
- Numbered options (doesn't match premium aesthetic)
- Mouse-only interface (doesn't meet efficiency requirements)