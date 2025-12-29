# ADR-0002: Task ID Generation: Sequential vs UUID

**Status**: Accepted
**Date**: 2025-12-11
**Authors**: Claude

## Context

Need unique identifiers for tasks in the in-memory todo console application. The application requires that each task has a unique ID that users can reference when performing operations like update, delete, and toggle completion. We need to decide between sequential integers, UUIDs, or timestamps.

## Decision

Use sequential integers starting from 1 for task IDs. This approach provides user-friendly, predictable identifiers that are easy to type and remember.

## Alternatives Considered

1. Sequential integers (1, 2, 3...): User-friendly, predictable, easy to type
2. UUIDs (universally unique identifiers): Globally unique, but hard to type and remember
3. Timestamps: Unique at the time of creation, but not sequential
4. Random numbers: Not predictable, potential for collisions if not properly managed

## Consequences

Positive:
- User-friendly IDs that are easy to remember and type
- Predictable sequence helps users understand task order
- Simple to implement and maintain
- Intuitive for console application users

Negative:
- IDs are not globally unique (not an issue for in-memory application)
- Deletion creates gaps in sequence (acceptable for this use case)
- Potential confusion if users expect continuous sequence
- Not suitable for distributed systems (not applicable for Phase I)

## References

- spec.md: Task entity definition
- plan.md: Data Model section
- data-model.md: Task Entity definition