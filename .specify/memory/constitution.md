<!--
  Sync Impact Report:
  - Version Change: 1.1.0 → 1.2.0
  - Modified Sections: Phase II section materially expanded with complete deliverables, acceptance criteria, and implementation requirements
  - Added Content:
    * Detailed Phase II acceptance criteria checklist
    * Frontend deliverables (ChatKit UI, chat page, message handling)
    * Backend deliverables (Chat endpoint, OpenAI Agents SDK, MCP server with 5 tools, Conversation & Message models)
    * Specifications deliverables (MCP tool specs, agent behavior spec, chat API spec)
    * Documentation deliverables (README, setup instructions, environment variables, testing guide)
    * Tests deliverables (MCP tool tests, agent behavior tests, chat endpoint tests, stateless verification tests)
  - Removed Sections: None
  - Templates Status:
    ✅ spec-template.md (reviewed, no changes needed - already compatible)
    ✅ plan-template.md (reviewed, no changes needed - Constitution Check section remains valid)
    ✅ tasks-template.md (reviewed, no changes needed - task discipline unchanged)
  - Follow-up TODOs: None - all placeholders resolved
  - Bump Rationale: MINOR version bump (new section expansion) - Phase II content materially expanded with detailed deliverables and acceptance criteria
-->

# Evolution of Todo — Constitution

## Core Principles

### I. Spec-Driven Development First (NON-NEGOTIABLE)

**All code MUST be generated from specifications using Claude Code.**

- Manual coding is prohibited; specifications are the executable source of truth.
- If generated output is incorrect, the specification MUST be refined; code MUST NOT be manually edited.
- Specifications define intent, constraints, and acceptance criteria before any implementation.
- Every feature begins with a complete spec.md before any code generation.

**Rationale**: Ensures consistency, repeatability, and clear separation between business requirements and implementation. Specifications become living documentation that directly drives code generation.

### II. Phase-Based Development Discipline (NON-NEGOTIABLE)

**Development MUST proceed incrementally through defined hackathon phases (Phase I through Phase V).**

- Each phase MUST have its own specification documents in `specs/<phase-name>/`.
- Features from future phases MUST NOT be implemented until that phase is reached.
- Backward compatibility MUST be preserved when advancing to new phases.
- No "phase leakage" — implementation scope is strictly limited to current phase requirements.

**Rationale**: Maintains focus, prevents scope creep, ensures deliverables match hackathon evaluation criteria at each checkpoint, and allows for progressive enhancement without breaking prior work.

### III. Documentation as Core Artifact (NON-NEGOTIABLE)

**Every feature MUST include clear, reusable documentation.**

- Specifications MUST articulate:
  - **Intent**: Why the feature exists (business/user value)
  - **Constraints**: Technical and business boundaries
  - **Acceptance Criteria**: Testable conditions for completion
- All documentation MUST be written in Markdown.
- Documentation MUST be maintained as specifications evolve.

**Rationale**: Documentation drives code generation quality and serves as the contract between human intent and AI execution. Clear documentation reduces ambiguity and improves generation accuracy.

### IV. Reusable Intelligence & Agent Skills

**Repeated workflows MUST be converted into reusable Claude skills or sub-agents.**

- When a workflow pattern repeats 3+ times, it MUST be evaluated for skill creation.
- MCP tools SHOULD only be compiled into skills when they provide measurable token savings (>20% reduction).
- Skills MUST be:
  - **Minimal**: Single, well-defined responsibility
  - **Focused**: Clear input/output contracts
  - **Stable**: Versioned and tested before use
- Skills MUST be documented in `.claude/skills/` with clear usage instructions.

**Rationale**: Reduces token consumption, increases consistency, and improves agent efficiency through reusable patterns. Prevents redundant context loading.

### V. AI Agent Governance

**AI agents MUST operate within clearly defined scopes with deterministic outputs.**

- Each agent MUST have a documented scope of responsibility.
- Agents MUST NOT perform actions outside their defined scope.
- Agent outputs MUST be:
  - **Deterministic**: Same input produces same output
  - **Spec-Compliant**: Strictly follows specification constraints
  - **Auditable**: Changes are traceable to specifications
- Multi-agent workflows MUST have explicit handoff contracts.

**Rationale**: Prevents unpredictable behavior, ensures accountability, and maintains trust in automated code generation processes.

### VI. Code Quality Standards

**Generated code MUST meet production-readiness standards even for MVP deliverables.**

- Code MUST be:
  - **Readable**: Clear naming, logical structure, self-documenting where possible
  - **Modular**: Single-responsibility components with clear interfaces
  - **Secure by Default**: No hardcoded secrets, input validation, safe defaults
  - **Production-Oriented**: Error handling, logging, graceful degradation
- Experimental or unsafe patterns are prohibited unless explicitly specified and justified.
- Code MUST follow language-specific best practices and idioms.

**Rationale**: Ensures hackathon deliverables are demonstrable, maintainable, and extensible. Avoids technical debt that would require manual refactoring.

### VII. Security & Privacy

**Security MUST be enforced by default across all phases.**

- Secrets, API keys, and credentials MUST NEVER be hardcoded in code or committed to version control.
- All secrets MUST be stored in environment variables or secure vaults (e.g., `.env` files in `.gitignore`).
- Input validation MUST be applied at system boundaries (user input, external APIs).
- AI features MUST NOT expose sensitive user data in logs, errors, or outputs.
- Basic security best practices MUST be followed:
  - Parameterized queries (SQL injection prevention)
  - Output encoding (XSS prevention)
  - Proper authentication and authorization checks
  - Rate limiting where appropriate

**Rationale**: Security vulnerabilities are unacceptable even in hackathon projects. Prevents credential leaks and establishes secure development habits from the start.

### VIII. Cloud-Native Readiness

**Architecture MUST support containerization and Kubernetes deployment from Phase I.**

- Applications MUST be designed to run in containers (Docker).
- Configuration MUST be environment-driven (12-factor principles).
- Services MUST be stateless where possible; state MUST be externalized.
- Kubernetes compatibility is mandatory for later phases:
  - Health check endpoints
  - Graceful shutdown handling
  - Configuration via ConfigMaps/Secrets
- Infrastructure-as-code patterns are encouraged.

**Rationale**: Ensures smooth transition from local development to cloud deployment. Aligns with hackathon's cloud-native evaluation criteria.

### IX. Performance & Token Efficiency

**Implementation MUST optimize for both runtime performance and AI token usage.**

- Avoid unnecessary verbose outputs in generated code (excessive comments, boilerplate).
- Specifications MUST be concise but complete — no redundant context.
- AI interactions MUST minimize token consumption:
  - Reuse established patterns via skills
  - Reference existing code rather than regenerating
  - Use targeted clarifications rather than broad re-specifications
- Runtime performance MUST meet phase-specific requirements defined in specifications.
- Performance budgets (latency, throughput, resource usage) MUST be documented when applicable.

**Rationale**: Token efficiency reduces costs and improves iteration speed. Runtime performance ensures user experience quality and scalability.

## Development Workflow

### Specification Workflow

1. **Specification Creation** (`/sp.specify`):
   - Define feature intent, constraints, and acceptance criteria in `specs/<feature>/spec.md`
   - Include user stories, functional requirements, and success criteria
   - Mark unclear requirements explicitly (e.g., `[NEEDS CLARIFICATION: ...]`)

2. **Implementation Planning** (`/sp.plan`):
   - Architect technical approach in `specs/<feature>/plan.md`
   - Document decisions, dependencies, and structure
   - Pass Constitution Check (verify compliance with all principles)
   - Identify Architecture Decision Records (ADRs) for significant decisions

3. **Task Breakdown** (`/sp.tasks`):
   - Generate actionable tasks in `specs/<feature>/tasks.md`
   - Organize by user story priority (P1, P2, P3...)
   - Include explicit dependencies and parallel opportunities

4. **Implementation** (`/sp.implement`):
   - Execute tasks via Claude Code
   - Validate against acceptance criteria
   - Create Prompt History Records (PHRs) for all significant interactions

5. **Commit & PR** (`/sp.git.commit_pr`):
   - Commit generated code with descriptive messages
   - Create pull requests with spec references
   - Ensure all artifacts are version-controlled

### Constitution Compliance

**Every planning phase MUST include a Constitution Check section verifying:**

- Spec-Driven Development: All code generated from specs
- Phase Discipline: No future-phase features included
- Documentation: Clear intent, constraints, acceptance criteria
- Security: No hardcoded secrets, secure defaults applied
- Cloud-Native: Containerization/Kubernetes considerations addressed
- Code Quality: Production-readiness standards met

Violations MUST be explicitly justified in `plan.md` with rationale and alternatives considered.

## Quality Standards

### Acceptance Criteria

**All features MUST define measurable acceptance criteria:**

- **Functional Completeness**: All specified behaviors implemented
- **Specification Compliance**: Generated code matches spec intent exactly
- **Security Verification**: No secrets in code, secure patterns applied
- **Documentation Coverage**: README, API docs, and usage examples provided
- **Phase Constraints**: No out-of-phase features present

### Testing Requirements

**Testing is OPTIONAL unless explicitly specified in feature requirements.**

When testing is required:
- Tests MUST be written BEFORE implementation (TDD if specified)
- Contract tests MUST cover public APIs and interfaces
- Integration tests MUST validate user journeys
- Tests MUST be organized by user story for independent validation

### Architecture Decision Records (ADRs)

**Significant architectural decisions SHOULD be documented as ADRs.**

A decision is significant if ALL conditions apply:
- **Impact**: Long-term consequences on system design
- **Alternatives**: Multiple viable options were considered
- **Scope**: Cross-cutting and influences multiple components

When detected, suggest: `📋 Architectural decision detected: [brief] — Document? Run /sp.adr [title]`

Wait for user consent; never auto-create ADRs.

## Phase II: Full-Stack Web Application

**Goal**: Transform console application to multi-user web application with authentication, REST API, and PostgreSQL persistence.

### Architecture Overview

- **Frontend**: Next.js 16+ App Router, Better Auth, TypeScript, Tailwind CSS
- **Backend**: FastAPI, SQLModel, JWT verification, Python
- **Database**: Neon Serverless PostgreSQL
- **Auth Flow**: Better Auth issues JWT → Frontend stores token → Backend verifies JWT and filters by user_id
- **Deployment**: Docker containers, docker-compose orchestration

### Phase II Deliverables

#### 1. Frontend Deliverables

- **ChatKit UI Component**: Reusable chat interface component
- **Chat Page Integration**: Full chat page with routing
- **Message Display**: Real-time message rendering with user attribution
- **Input Handling**: Message composition and submission with validation

#### 2. Backend Deliverables

- **Chat Endpoint**: RESTful API for chat operations (send, retrieve, history)
- **OpenAI Agents SDK**: Integration with OpenAI Agents framework
- **MCP Server**: Model Context Protocol server with 5 production-ready tools:
  - Tool 1: Task creation/management
  - Tool 2: Task retrieval/search
  - Tool 3: Task status updates
  - Tool 4: Task deletion
  - Tool 5: Analytics/reporting
- **Conversation & Message Models**: SQLModel entities for chat persistence
- **Database Migrations**: Alembic migrations for schema evolution

#### 3. Specifications Deliverables

- **MCP Tool Specs**: Detailed specification for each MCP tool (inputs, outputs, behavior)
- **Agent Behavior Spec**: Agent personality, constraints, conversation flow
- **Chat API Spec**: OpenAPI/REST contract definitions
- **Natural Language Examples**: Sample interactions demonstrating expected behavior

#### 4. Documentation Deliverables

- **README Updated**: Installation, setup, and usage instructions
- **Setup Instructions**: Step-by-step local and Docker setup
- **Environment Variables**: Complete `.env.example` with all required variables
- **Testing Guide**: How to run and validate tests

#### 5. Tests Deliverables

- **MCP Tool Tests**: Unit tests for each MCP tool (contract verification)
- **Agent Behavior Tests**: Conversation flow and response quality tests
- **Chat Endpoint Tests**: API integration tests (auth, CRUD, error handling)
- **Stateless Verification Tests**: Ensure agent operates without hidden state dependencies

### Phase II Acceptance Criteria

**All items MUST be satisfied before Phase II is considered complete:**

- [ ] Frontend chat UI renders correctly in all target browsers
- [ ] Users can authenticate via Better Auth and receive JWT
- [ ] JWT tokens are validated on every backend request
- [ ] Chat messages are persisted to PostgreSQL database
- [ ] MCP server exposes all 5 tools with correct contracts
- [ ] OpenAI Agent SDK correctly invokes MCP tools
- [ ] Agent responses are contextually relevant and user-specific
- [ ] All database migrations run successfully without errors
- [ ] Docker containers build and start via `docker-compose up`
- [ ] Environment variables documented in `.env.example`
- [ ] All tests pass (MCP tools, agent behavior, chat endpoints, stateless verification)
- [ ] API returns user-friendly error messages with appropriate status codes
- [ ] Error handling is graceful (no crashes, proper logging)
- [ ] All database migrations applied successfully

### Phase II Implementation Notes

**Authentication Flow**:
1. User logs in via Better Auth (frontend)
2. Better Auth issues JWT token
3. Frontend stores JWT in memory/localStorage
4. Every API call includes `Authorization: Bearer <token>` header
5. Backend verifies JWT signature and extracts user_id
6. All database queries filter by authenticated user_id

**Stateless Agent Design**:
- Agent MUST NOT maintain conversation state between requests
- All context MUST be passed explicitly in each request
- Conversation history stored in database, retrieved per request
- MCP tools MUST be pure functions (deterministic, side-effect declarations)

**Development Sequence** (per Spec-Driven Development workflow):
1. Create Phase II specifications in `specs/phase-ii/`
2. Design database schema and migrations
3. Implement backend API (auth, chat endpoints, MCP server)
4. Implement frontend (auth integration, ChatKit component, chat page)
5. Integrate OpenAI Agents SDK with MCP server
6. Write and validate all tests
7. Update documentation and environment setup
8. Validate acceptance criteria checklist

## Governance

**This Constitution supersedes all other practices and preferences.**

- All specifications, plans, and tasks MUST verify compliance with Constitution principles.
- Pull requests MUST reference Constitution sections to demonstrate alignment.
- Complexity not covered by Constitution MUST be explicitly justified in planning artifacts.
- Amendments require:
  - Documentation of rationale in Constitution itself
  - User approval via Prompt History Record (PHR)
  - Migration plan for affected specifications and code
  - Version increment following semantic versioning

### Amendment Process

- **MAJOR** version (X.0.0): Breaking changes to core principles, removals, or redefinitions
- **MINOR** version (0.X.0): New principles added or material expansions
- **PATCH** version (0.0.X): Clarifications, wording improvements, non-semantic fixes

### Compliance Review

- Constitution compliance is MANDATORY at planning phase (`/sp.plan`)
- Violations MUST be justified or resolved before implementation proceeds
- Agents MUST refuse to generate code that violates principles without explicit user override
- Users MAY request principle waivers for specific features with documented justification

**Version**: 1.2.0 | **Ratified**: 2025-12-29 | **Last Amended**: 2025-12-31
