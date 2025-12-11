# ADR-0003: Menu System: Loop vs State Machine

**Status**: Accepted
**Date**: 2025-12-11
**Authors**: Claude

## Context

Need to implement an interactive CLI interface for the todo console application. Users need to navigate between different operations (add, view, update, delete, mark complete) through a menu system. We need to decide between a simple while loop with if/elif statements, a state machine pattern, or using a CLI framework.

## Decision

Use a simple while loop with numbered menu options. This approach provides a straightforward, easy-to-understand implementation that meets the requirements without adding unnecessary complexity.

## Alternatives Considered

1. While loop with numbered menu: Simple, no external dependencies, easy to understand
2. State machine pattern: More structured, but adds complexity for simple navigation
3. CLI framework (argparse, click, etc.): Feature-rich but overkill for console menu interface
4. Direct command input: Requires users to remember commands, less user-friendly

## Consequences

Positive:
- Simple implementation that's easy to understand and maintain
- No external dependencies required (aligns with Python stdlib-only requirement)
- Clear, intuitive interface with numbered options
- Easy to extend with additional menu options
- Predictable user experience

Negative:
- Manual input handling and validation required
- More verbose than using a CLI framework
- Less sophisticated than state machine approach
- Requires careful error handling for invalid inputs

## References

- spec.md: User interaction requirements
- plan.md: UI Layer and MenuSystem component
- plan.md: Data Flow section