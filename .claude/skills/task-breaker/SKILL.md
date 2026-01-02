---
name: task-breaker
description: Break down implementation plans into small, ordered, dependency-aware tasks optimized for /sp.tasks.
version: 1.0
---

## When to Use
- When /sp.tasks output is too generic or vague
- When tasks are too large to implement safely
- When tasks need clear ordering and dependencies
- Before calling /sp.implement

## Procedure
1. Read the implementation plan carefully
2. Identify major components (e.g., models, services, UI, APIs)
3. Break each component into atomic, single-responsibility tasks
4. Order tasks logically (foundations first, integrations later)
5. Explicitly mention dependencies between tasks
6. Avoid combining frontend, backend, and infra tasks together

## Output Format
- Numbered list of tasks
- Each task must:
  - Be implementable in one step
  - Mention dependencies (if any)
  - Be clear enough for direct execution by /sp.implement

## Constraints
- Do NOT write code
- Do NOT repeat the plan
- Do NOT create abstract or conceptual tasks
