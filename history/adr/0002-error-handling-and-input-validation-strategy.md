# ADR-0002: Error Handling and Input Validation Strategy

> **Scope**: This ADR documents the integrated error handling and validation approach, combining exception-based error propagation with modular input validation for the console application.

- **Status:** Accepted
- **Date:** 2025-12-30
- **Feature:** 001-in-memory-todo
- **Context:** Phase I requires robust error handling for user inputs (descriptions, IDs, menu choices) and clear error messaging as specified in FR-012. The solution must gracefully handle all invalid inputs without crashes (SC-004), provide actionable error messages (SC-003), and maintain code quality through separation of concerns.

<!-- Significance checklist (ALL must be true to justify this ADR)
     ✅ 1) Impact: Long-term consequence - establishes error handling patterns for all future phases
     ✅ 2) Alternatives: Multiple viable options considered (exceptions vs return codes vs Result types, inline vs module validation)
     ✅ 3) Scope: Cross-cutting concern - affects all layers (models, managers, CLI, error display)
-->

## Decision

**Integrated Error Handling & Validation Strategy** combining two related decisions:

1. **Error Handling**: Exception-based approach with custom exception classes
2. **Input Validation**: Separate `validators.py` module with reusable validation functions

```python
# Custom exceptions for clear error cases
class TaskNotFoundError(Exception):
    """Raised when task ID doesn't exist"""
    pass

class InvalidDescriptionError(Exception):
    """Raised when description validation fails"""
    pass

class InvalidInputError(Exception):
    """Raised for general input validation failures"""
    pass

# Separate validation module (src/cli/validators.py)
def validate_description(description: str) -> str:
    """Validate task description (1-200 chars, non-empty)"""
    # Returns sanitized description or raises InvalidDescriptionError

def validate_task_id(id_input: str) -> int:
    """Validate and parse task ID input"""
    # Returns parsed ID or raises InvalidInputError

def validate_menu_choice(choice_input: str, max_choice: int) -> int:
    """Validate menu choice is within valid range"""
    # Returns parsed choice or raises InvalidInputError
```

## Consequences

### Positive

- **Clarity**: Custom exceptions provide specific error types (TaskNotFoundError, InvalidDescriptionError)
- **Pythonic**: Idiomatic Python error handling (try/except) familiar to developers
- **Separation of Concerns**: Validation logic isolated in dedicated module, reusable across CLI commands
- **Testability**: Validators independently testable without UI coupling
- **Error Messages**: Clear error types enable specific, actionable user messages (FR-012 compliant)
- **Debugging**: Stack traces available for development without exposing implementation to users
- **Happy Path Clarity**: Error handling separated from main logic flow
- **Reusability**: Validation functions used across multiple CLI operations (add, update, etc.)

### Negative

- **Exception Overhead**: Slightly higher performance cost than return codes (negligible for console app)
- **Learning Curve**: Developers must understand custom exception hierarchy
- **Try/Except Blocks**: Requires explicit exception handling in calling code (enforces error handling)
- **No Type Checking**: Exceptions not tracked by type system (mitigated: clear docstrings, consistent naming)

## Alternatives Considered

### Alternative Error Handling A: Return Codes (C-style)
- **Components**: Functions return 0 for success, -1 for error; separate error message variable
- **Rejected because**: Error-prone (easy to ignore return codes), mixes success/error logic in same flow, not Pythonic, requires manual error message propagation, harder to maintain.

### Alternative Error Handling B: Result Objects (Rust-style)
- **Components**: `Result[T, E]` type with `Ok(value)` and `Err(error)` variants
- **Rejected because**: Requires custom implementation or external library (violates stdlib-only constraint), overkill for simple console app, less familiar to Python developers, verbose for simple cases.

### Alternative Error Handling C: Silent Failure with Logging
- **Components**: Catch errors, log them, continue execution
- **Rejected because**: Violates spec requirement for clear user-facing error messages (FR-012), poor user experience (no feedback on invalid input), debugging nightmare, unacceptable for production-oriented code.

### Alternative Validation A: Inline Validation in CLI
- **Components**: Validation logic embedded directly in menu/command handling functions
- **Rejected because**: Tight coupling between validation and UI, code duplication across commands, hard to test in isolation, violates single-responsibility principle.

### Alternative Validation B: Validation Methods in Task Model
- **Components**: `Task.validate_description()`, `Task.validate_status()` class methods
- **Rejected because**: Mixes data representation with UI-specific validation concerns, Task model shouldn't know about user input formats, reduces model reusability.

### Alternative Validation C: Decorator-based Validation
- **Components**: `@validate_description` decorators on CLI methods
- **Rejected because**: Over-engineered for simple validation needs, adds complexity without benefit, harder to understand for spec-driven code generation, overkill for Phase I scope.

## References

- Feature Spec: [specs/001-in-memory-todo/spec.md](../../specs/001-in-memory-todo/spec.md) (FR-005, FR-012, SC-003, SC-004)
- Implementation Plan: [specs/001-in-memory-todo/plan.md](../../specs/001-in-memory-todo/plan.md#decision-4-input-validation-strategy)
- Related ADRs: ADR-0001 (Data Architecture - Task model validation)
- Evaluator Evidence: Plan Phase 0 (Decisions 4-5), Constitution Check (Principle VI: Code Quality Standards)
