# ADR-0001: Data Structure Choice: List vs Dictionary for Task Storage

**Status**: Accepted
**Date**: 2025-12-11
**Authors**: Claude

## Context

Need to store multiple tasks efficiently in the in-memory todo console application. The application requires storing Task objects with the ability to perform CRUD operations. We need to decide between using a list of dictionaries, a dictionary with ID keys, or a custom class with internal list storage.

## Decision

Use a list of Task dataclass objects for storage. This approach provides type safety through dataclasses, maintains order, and allows for simple iteration and searching operations.

## Alternatives Considered

1. List of dictionaries: Simple but lacks type safety and structure
2. Dictionary with ID keys: Provides O(1) lookup by ID but loses insertion order
3. Custom class with internal list: Adds unnecessary complexity for this use case
4. Using a database: Overly complex for Phase I in-memory requirement

## Consequences

Positive:
- Type safety with dataclasses improves code reliability
- Simple iteration and searching operations
- Maintains insertion order of tasks
- Easy to understand and maintain

Negative:
- O(n) lookup by ID (acceptable for small datasets)
- Deletion creates gaps in sequential access
- Requires iteration for ID-based operations

## References

- plan.md: Data Model section
- plan.md: System Architecture section
- data-model.md: Task Entity definition