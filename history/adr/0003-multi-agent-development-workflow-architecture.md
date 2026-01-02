# ADR-0003: Multi-Agent Development Workflow Architecture

> **Scope**: This ADR documents the complete multi-agent workflow architecture including agent specialization, model selection strategy, and handoff protocols for spec-driven development.

- **Status:** Accepted
- **Date:** 2025-12-30
- **Feature:** 001-in-memory-todo
- **Context:** Phase I requires implementing spec-driven development with reusable intelligence across all 5 hackathon phases. The solution must optimize both code quality and token efficiency, enable parallel workflows, and maintain clear separation of concerns across design, implementation, testing, and documentation activities.

<!-- Significance checklist (ALL must be true to justify this ADR)
     ✅ 1) Impact: Long-term consequence - establishes development workflow for all 5 phases, reusable agent patterns
     ✅ 2) Alternatives: Multiple viable options considered (single agent vs multi-agent, model selection strategies)
     ✅ 3) Scope: Cross-cutting concern - affects all development activities (design, code, test, docs)
-->

## Decision

**Multi-Agent Development Workflow** combining agent specialization with strategic model selection:

**Agent Architecture** (4 specialized agents):
1. **Architect Agent** (Claude 3.5 Sonnet) - Design & architectural decisions
2. **Developer Agent** (Claude 3.5 Sonnet) - Code generation from specifications
3. **Tester Agent** (Claude 3.5 Haiku) - Test generation & validation
4. **Reviewer Agent** (Claude 3.5 Sonnet) - Quality assurance & integration

**Model Selection Strategy**:
- Critical/Complex tasks (design, code generation, review): Claude 3.5 Sonnet
- Simple/Repetitive tasks (test generation, documentation): Claude 3.5 Haiku
- Reasoning: Balance quality where needed with token efficiency for routine tasks

**Workflow Sequence**:
```
Architect (Sonnet) → Developer (Sonnet) → Tester (Haiku) → Reviewer (Sonnet)
     ↓                    ↓                     ↓                  ↓
  Design Specs      Implementation         Test Suite        Integration
```

**Handoff Contracts**:
- Architect → Developer: Complete specs (data-model.md, contracts/)
- Developer → Tester: Source code + specs
- Tester → Reviewer: Source + tests (must pass)
- Reviewer validates against constitution and spec compliance

## Consequences

### Positive

- **Quality Optimization**: Sonnet used for critical decisions (architecture, code, review) ensures high-quality outputs
- **Token Efficiency**: Haiku for tests saves 40-50% tokens vs all-Sonnet approach
- **Expertise Focus**: Each agent specialized in specific domain (design vs code vs test vs review)
- **Reusability**: Agent patterns and workflows reusable across all 5 phases
- **Parallel Workflows**: Independent agents can work concurrently where dependencies allow
- **Clear Ownership**: Each agent has defined scope, preventing overlap and confusion
- **Constitution Compliance**: Reviewer agent enforces all 9 constitution principles
- **Deterministic Outputs**: Spec-driven approach ensures consistent results
- **Auditability**: Clear handoff points enable tracing decisions through workflow
- **Scalability**: Adding new agents (e.g., Security Agent) follows established pattern

### Negative

- **Initial Setup Overhead**: Requires defining 4 agent configs and handoff protocols
- **Coordination Complexity**: Must manage handoffs and ensure data flows correctly
- **Sequential Bottlenecks**: Some workflows inherently sequential (can't test before code exists)
- **Model Switching Cost**: Context loss between agent handoffs (mitigated: explicit data transfer)
- **Debugging Challenge**: Errors may span multiple agents, requiring trace-through
- **Over-Engineering Risk**: 4 agents may be overkill for simple tasks (mitigated: agents optional for trivial changes)

## Alternatives Considered

### Alternative A: Single Monolithic Agent (All Sonnet)
- **Components**: One agent performs all tasks (design, code, test, docs) using Sonnet
- **Rejected because**:
  - No specialization, harder to optimize per task
  - All tasks use expensive Sonnet model (no token savings)
  - Less focused outputs, mixed concerns in single context
  - Doesn't leverage Constitutional principle IV (Reusable Intelligence)

### Alternative B: Micro-Agent Architecture (10+ Agents)
- **Components**: Highly specialized agents for each subtask (ModelDesigner, CodeWriter, TestWriter, UnitTester, IntegrationTester, DocWriter, Reviewer, etc.)
- **Rejected because**:
  - Over-engineered for Phase I scope
  - Excessive handoff complexity and coordination overhead
  - Diminishing returns beyond 4-5 agents
  - Higher total token cost from context switching

### Alternative C: All Haiku Model Strategy
- **Components**: 4 agents, all using Haiku model
- **Rejected because**:
  - Insufficient quality for critical tasks (architecture, code generation)
  - Higher error rates requiring rework (negates token savings)
  - Doesn't meet code quality standards (Constitution VI)

### Alternative D: All Opus Model Strategy
- **Components**: 4 agents, all using Opus model
- **Rejected because**:
  - Prohibitively expensive for hackathon project
  - Overkill for simple tasks (tests, docs)
  - Opus quality not meaningfully better than Sonnet for this scope
  - Violates Constitution IX (token efficiency)

### Alternative E: Mixed Model Strategy B (Opus + Sonnet + Haiku)
- **Components**: Architect uses Opus, Developer uses Sonnet, Tester/Reviewer use Haiku
- **Rejected because**:
  - Opus cost unjustified (Sonnet sufficient for architecture)
  - Haiku insufficient for review/quality assurance
  - More complex model management
  - Quality regression on critical review step

## References

- Feature Spec: [specs/001-in-memory-todo/spec.md](../../specs/001-in-memory-todo/spec.md) (Constitution requirements)
- Implementation Plan: [specs/001-in-memory-todo/plan.md](../../specs/001-in-memory-todo/plan.md#multi-agent-workflow)
- Constitution: [.specify/memory/constitution.md](../../.specify/memory/constitution.md) (Principles IV, V, IX)
- Related ADRs: None (workflow-level decision)
- Evaluator Evidence: Plan Multi-Agent Workflow section, Constitution Check (Principles IV & V passed)
