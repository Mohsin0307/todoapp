# ADR-0001: Data Architecture for In-Memory Task Storage

> **Scope**: This ADR documents the complete data architecture cluster including storage structure, ID generation strategy, and status representation for the Phase I in-memory todo application.

- **Status:** Accepted
- **Date:** 2025-12-30
- **Feature:** 001-in-memory-todo
- **Context:** Phase I requires a simple, performant in-memory data architecture for managing todo tasks in a console application. The solution must support <100ms CRUD operations, handle 1000+ tasks, use only Python stdlib, and provide a clear migration path to persistence in future phases.

<!-- Significance checklist (ALL must be true to justify this ADR)
     ✅ 1) Impact: Long-term consequence - establishes data model that future phases will extend
     ✅ 2) Alternatives: Multiple viable options considered (dict vs list, UUID vs auto-increment, enum vs strings)
     ✅ 3) Scope: Cross-cutting concern - affects all components (models, managers, CLI, tests)
-->

## Decision

**Integrated Data Architecture** combining three related decisions:

1. **Storage Structure**: Use `dict[int, Task]` with task ID as key for in-memory storage
2. **ID Generation**: Auto-incrementing integer counter starting at 1
3. **Status Representation**: String literals ("pending", "completed")

```python
class TaskManager:
    def __init__(self):
        self._tasks: dict[int, Task] = {}  # Storage
        self._next_id: int = 1              # ID generator

@dataclass
class Task:
    id: int
    description: str
    status: str = "pending"  # Status representation
```

## Consequences

### Positive

- **Performance**: O(1) lookup, insertion, deletion by ID (meets <100ms requirement)
- **Simplicity**: Standard library only, no external dependencies
- **Readability**: String statuses match spec terminology exactly ("pending", "completed")
- **User Experience**: Sequential IDs (1, 2, 3...) are intuitive in console interface
- **Extensibility**: Easy to add new statuses ("in_progress", "archived") without code changes
- **Migration Path**: Dict structure can be replaced with database ORM in future phases
- **Memory Efficiency**: Suitable for 1000+ tasks without performance degradation
- **Spec Compliance**: Explicitly required by FR-001 (sequential integer ID starting from 1)

### Negative

- **No Persistence**: Data lost on application exit (acceptable for Phase I by design)
- **No Universal Uniqueness**: IDs not unique across sessions (mitigated: single-session scope)
- **Type Safety**: String statuses lack compile-time checking (mitigated: validation in Task.__post_init__)
- **Memory vs List**: Slightly higher memory overhead than list (negligible for 1000 tasks)
- **Ordering**: No explicit creation time tracking (mitigated: dict preserves insertion order in Python 3.7+)

## Alternatives Considered

### Alternative Storage Structure A: List-based with linear search
- **Components**: `List[Task]`, find by ID via iteration
- **Rejected because**: O(n) lookup performance violates <100ms requirement for large task lists. Update and delete operations require list scanning and reindexing.

### Alternative Storage Structure B: SQLite database
- **Components**: SQLite file, SQL queries, ORM
- **Rejected because**: Adds file I/O complexity, requires external dependency or sql library, violates Phase I constraint of in-memory only. Overkill for console MVP.

### Alternative ID Strategy A: UUID-based
- **Components**: UUID4 generation, string-based IDs
- **Rejected because**: Not user-friendly in console (long hex strings), violates spec requirement for "sequential integer ID", unnecessary global uniqueness for single-session application.

### Alternative ID Strategy B: Timestamp-based
- **Components**: Millisecond timestamp as ID
- **Rejected because**: Not guaranteed unique, complex to display, doesn't match user mental model of task numbering (1, 2, 3...).

### Alternative Status Strategy A: Boolean flag
- **Components**: `is_completed: bool`
- **Rejected because**: Semantically limited (what about "in_progress" in future?), less readable than explicit status strings, doesn't align with spec terminology.

### Alternative Status Strategy B: Enum class
- **Components**: `TaskStatus(Enum)` with PENDING, COMPLETED members
- **Rejected because**: Adds complexity without benefit for 2 states, requires additional import, potentially more complex for spec-driven code generation.

## References

- Feature Spec: [specs/001-in-memory-todo/spec.md](../../specs/001-in-memory-todo/spec.md)
- Implementation Plan: [specs/001-in-memory-todo/plan.md](../../specs/001-in-memory-todo/plan.md#phase-0-research--technology-decisions)
- Related ADRs: None (first ADR for this feature)
- Evaluator Evidence: Constitution Check in plan.md (all gates passed), Research Phase 0 (Decisions 1-3)
