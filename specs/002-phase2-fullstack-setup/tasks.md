# Tasks: Phase II Full-Stack Web Application Setup

**Input**: Design documents from `/specs/002-phase2-fullstack-setup/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/api-spec.yaml

**Tests**: Tests are NOT requested in the specification - implementation only

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `- [ ] [ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

This is a **monorepo web application** with:
- `backend/` - Python FastAPI service
- `frontend/` - Next.js TypeScript application
- Root-level configuration and documentation

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and monorepo structure

- [X] T001 Create monorepo directory structure (backend/, frontend/, preserve src/ and tests/ from Phase I)
- [X] T002 [P] Create root .gitignore file (exclude .env, node_modules, __pycache__, .next, .venv)
- [X] T003 [P] Create root .env.example with placeholder environment variables
- [X] T004 Initialize backend Python project in backend/pyproject.toml with FastAPI, SQLModel, alembic, pytest dependencies
- [X] T005 Initialize frontend Next.js project in frontend/package.json with Next.js 16, TypeScript, Tailwind, Better Auth dependencies
- [X] T006 [P] Configure TypeScript strict mode in frontend/tsconfig.json
- [X] T007 [P] Configure Tailwind CSS in frontend/tailwind.config.js
- [X] T008 [P] Create backend/.env.example with DATABASE_URL, JWT_SECRET, ALLOWED_ORIGINS placeholders
- [X] T009 [P] Create frontend/.env.local.example with NEXT_PUBLIC_API_URL, BETTER_AUTH_SECRET placeholders

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Backend Foundation

- [X] T010 Create backend/main.py with FastAPI app initialization and CORS middleware configuration
- [X] T011 [P] Create backend/src/__init__.py as Python package marker
- [X] T012 [P] Create backend/src/config.py with Pydantic BaseSettings for environment variables (DATABASE_URL, JWT_SECRET, ALLOWED_ORIGINS)
- [X] T013 Create backend/src/database.py with async SQLAlchemy engine and session dependency injection
- [X] T014 Initialize Alembic in backend/alembic/ for database migrations
- [X] T015 Create backend/src/models/__init__.py as models package
- [X] T016 Create backend/src/models/task.py with SQLModel Task entity (id, user_id, title, description, completed, created_at, updated_at, deleted_at)
- [X] T017 Create Alembic migration for tasks table in backend/alembic/versions/001_create_tasks_table.py (includes indexes and constraints)
- [X] T018 [P] Create backend/src/middleware/__init__.py as middleware package
- [X] T019 Create backend/src/middleware/auth.py with JWT verification middleware (extracts user_id from Bearer token)
- [X] T020 [P] Create backend/src/services/__init__.py as services package
- [X] T021 Create backend/src/services/task_service.py with user-scoped CRUD operations (create, get_all, get_by_id, update, delete, toggle_completion)
- [X] T022 [P] Create backend/src/api/__init__.py as API package
- [X] T023 Create backend/src/api/health.py with GET /health endpoint (no authentication required)
- [X] T024 Create backend/src/api/tasks.py with 6 REST endpoints (GET /api/tasks, POST /api/tasks, GET /api/tasks/{id}, PUT /api/tasks/{id}, DELETE /api/tasks/{id}, PATCH /api/tasks/{id}/complete)
- [X] T025 Register task routes in backend/main.py with /api prefix and authentication middleware

### Frontend Foundation

- [X] T026 Create frontend/app/layout.tsx as root layout with metadata and Better Auth provider
- [X] T027 [P] Create frontend/lib/auth.ts with Better Auth client configuration (JWT plugin, httpOnly cookies)
- [X] T028 [P] Create frontend/lib/api.ts with API client (base URL from env, JWT token injection interceptor, error handling)
- [X] T029 Create frontend/app/page.tsx as landing page with links to login/signup
- [X] T030 [P] Create frontend/app/login/page.tsx with Better Auth login form
- [X] T031 [P] Create frontend/app/signup/page.tsx with Better Auth signup form
- [X] T032 Create frontend/app/tasks/page.tsx as protected task list page (redirects to login if unauthenticated)
- [X] T033 [P] Create frontend/components/TaskList.tsx to display tasks with loading states
- [X] T034 [P] Create frontend/components/TaskForm.tsx for create/edit task with react-hook-form validation
- [X] T035 [P] Create frontend/components/TaskItem.tsx for individual task card with complete/delete actions

### Docker & DevOps Foundation

- [X] T036 Create docker-compose.yml with backend and frontend services (ports 8000 and 3000, volume mounts for hot reload, env_file references)
- [X] T037 [P] Create backend/Dockerfile with Python 3.11 base image, dependency installation, uvicorn command
- [X] T038 [P] Create frontend/Dockerfile with Node 18 base image, dependency installation, npm run dev command

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Project Infrastructure Initialization (Priority: P1) 🎯 MVP

**Goal**: Complete project infrastructure set up so developers can begin implementing authentication and task management features

**Independent Test**: Verify all configuration files exist, directories are created, and documentation is accessible

**Note**: Most infrastructure was created in Setup (Phase 1) and Foundational (Phase 2). This phase validates and documents the setup.

### Implementation for User Story 1

- [ ] T039 [P] [US1] Validate .spec-kit/config.yaml exists with correct content (project name, version 2.0, phases, agents)
- [ ] T040 [P] [US1] Validate CLAUDE.md exists at root with monorepo layout, development workflow, technologies, running instructions
- [ ] T041 [P] [US1] Validate specs/overview.md exists with Phase II objectives, architecture, user flow, API endpoints, success criteria
- [ ] T042 [P] [US1] Validate all spec subdirectories exist (specs/features/, specs/api/, specs/database/, specs/ui/)
- [ ] T043 [US1] Create backend/CLAUDE.md with backend-specific development guide (FastAPI structure, SQLModel usage, JWT verification, running uvicorn, pytest commands)
- [ ] T044 [US1] Create frontend/CLAUDE.md with frontend-specific development guide (Next.js App Router, Better Auth integration, API client usage, running npm dev, component structure)
- [ ] T045 [US1] Test Docker Compose startup (docker-compose up --build) and verify both services start successfully
- [ ] T046 [US1] Test database migration (docker-compose exec backend alembic upgrade head) and verify tasks table created
- [ ] T047 [US1] Test backend health endpoint (GET http://localhost:8000/health) returns {"status": "healthy"}
- [ ] T048 [US1] Test frontend loads (http://localhost:3000) and displays landing page

**Acceptance Criteria** (from spec.md):
1. ✓ All configuration files (.spec-kit/config.yaml, CLAUDE.md) created with correct content
2. ✓ overview.md and all subdirectories (features/, api/, database/, ui/) exist
3. ✓ Developer can read CLAUDE.md and understand monorepo layout, development workflow, authentication flow

**Checkpoint**: At this point, User Story 1 is complete - full infrastructure is operational and documented

---

## Phase 4: User Story 2 - Development Agent Configuration (Priority: P1)

**Goal**: Specialized agents configured so different aspects of the system can be developed by appropriate expertise

**Independent Test**: Verify .spec-kit/config.yaml contains all four agents with correct roles and models

**Note**: Agent configuration was created during /sp.specify. This phase validates the configuration.

### Implementation for User Story 2

- [ ] T049 [P] [US2] Validate .spec-kit/config.yaml has backend-developer agent with role "FastAPI backend implementation" and model "claude-3-5-sonnet-20241022"
- [ ] T050 [P] [US2] Validate .spec-kit/config.yaml has frontend-developer agent with role "Next.js frontend implementation" and model "claude-3-5-sonnet-20241022"
- [ ] T051 [P] [US2] Validate .spec-kit/config.yaml has database-architect agent with role "Database schema design" and model "claude-3-5-sonnet-20241022"
- [ ] T052 [P] [US2] Validate .spec-kit/config.yaml has api-designer agent with role "REST API specification" and model "claude-3-5-sonnet-20241022"
- [ ] T053 [US2] Document agent role mappings in specs/002-phase2-fullstack-setup/agent-roles.md (map each agent to specific implementation tasks from tasks.md)

**Acceptance Criteria** (from spec.md):
1. ✓ All four agents are defined with appropriate roles
2. ✓ Each agent's role clearly maps to specific development tasks

**Checkpoint**: At this point, User Stories 1 AND 2 are complete - infrastructure operational and agents configured

---

## Phase 5: User Story 3 - Phase Tracking and Documentation (Priority: P2)

**Goal**: Clear phase tracking so stakeholders can understand project progress and what has been completed versus what remains

**Independent Test**: Read config.yaml phases section and verify Phase I is marked completed and Phase II is marked in-progress

**Note**: Phase configuration was created during /sp.specify. This phase validates tracking and enhances documentation.

### Implementation for User Story 3

- [ ] T054 [P] [US3] Validate .spec-kit/config.yaml phases section shows phase1-console with status "completed" and features ["task-crud-cli"]
- [ ] T055 [P] [US3] Validate .spec-kit/config.yaml phases section shows phase2-web with status "in-progress" and features ["authentication", "task-crud-api", "task-crud-ui", "database-setup"]
- [ ] T056 [US3] Create README.md at repository root with Phase II overview, quick start instructions, technology stack, project structure, development workflow
- [ ] T057 [US3] Update specs/overview.md success criteria section with checkboxes (convert from spec.md SC-001 through SC-010)
- [ ] T058 [US3] Create specs/002-phase2-fullstack-setup/phase-progress.md tracking completion status of each Phase II feature (authentication, task-crud-api, task-crud-ui, database-setup)

**Acceptance Criteria** (from spec.md):
1. ✓ Phase I shows status "completed" with task-crud-cli feature
2. ✓ Phase II shows status "in-progress" with four planned features
3. ✓ overview.md has success criteria clearly defined and measurable

**Checkpoint**: All user stories are now complete - infrastructure, agents, and tracking fully operational

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and final validation

- [ ] T059 [P] Add comprehensive comments to backend/src/middleware/auth.py explaining JWT verification logic
- [ ] T060 [P] Add comprehensive comments to frontend/lib/api.ts explaining token injection and error handling
- [ ] T061 [P] Add type annotations to all backend service methods in backend/src/services/task_service.py
- [ ] T062 [P] Add JSDoc comments to all frontend utility functions in frontend/lib/utils.ts (if created)
- [ ] T063 Test complete user flow per quickstart.md (signup → login → create task → update task → toggle completion → delete task)
- [ ] T064 [P] Validate all environment variable examples in .env.example files match actual required variables
- [ ] T065 [P] Run backend code formatter (ruff format backend/src/) and linter (ruff check backend/src/)
- [ ] T066 [P] Run frontend code formatter (npm run lint frontend/) and type checker (npm run type-check in frontend/)
- [ ] T067 Verify Docker Compose services restart successfully after code changes (test hot reload)
- [ ] T068 [P] Update quickstart.md troubleshooting section with any new issues encountered during implementation
- [ ] T069 Run security check (verify no .env files in git, no hardcoded secrets in code)
- [ ] T070 Run quickstart.md validation (follow setup steps from scratch, verify all commands work)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational (Phase 2) completion
- **User Story 2 (Phase 4)**: Depends on Foundational (Phase 2) completion - Can run in parallel with US1
- **User Story 3 (Phase 5)**: Depends on Foundational (Phase 2) completion - Can run in parallel with US1/US2
- **Polish (Phase 6)**: Depends on all user stories (Phase 3, 4, 5) being complete

### Critical Path

```
Setup (Phase 1)
    ↓
Foundational (Phase 2) ← BLOCKING - Must complete before any user story
    ↓
    ├─→ User Story 1 (Phase 3) ─┐
    ├─→ User Story 2 (Phase 4) ─┼─→ All US Complete
    └─→ User Story 3 (Phase 5) ─┘
                ↓
        Polish (Phase 6)
```

### User Story Dependencies

- **User Story 1 (P1)**: Depends on Foundational (Phase 2) - Infrastructure validation and documentation
- **User Story 2 (P1)**: Depends on Foundational (Phase 2) - Agent configuration validation (can run parallel with US1)
- **User Story 3 (P2)**: Depends on Foundational (Phase 2) - Phase tracking and documentation (can run parallel with US1/US2)

**Note**: User Stories 1, 2, and 3 have NO dependencies on each other - they can all run in parallel once Foundational phase completes.

### Within Each Phase

**Phase 1 (Setup)**:
- T002-T009 marked [P] can all run in parallel after T001 completes

**Phase 2 (Foundational)**:
- Backend models/services: T012-T017 (backend structure) → T021 (services using models) → T024 (API using services)
- Frontend components: T027-T028 (auth/API clients) → T030-T031 (login/signup pages) → T033-T035 (task components)
- Docker: T037-T038 can run in parallel at any time

**Phase 3 (US1)**:
- T039-T042 (validations) can run in parallel
- T043-T044 (CLAUDE.md files) can run in parallel
- T045-T048 (tests) should run sequentially after infrastructure tasks

**Phase 4 (US2)**:
- T049-T052 (agent validations) can all run in parallel
- T053 depends on T049-T052

**Phase 5 (US3)**:
- T054-T055 (phase validations) can run in parallel
- T056-T058 (documentation) can run in parallel after validations

**Phase 6 (Polish)**:
- T059-T062, T064-T066, T068-T069 can all run in parallel
- T063, T067, T070 (tests/validations) should run after code tasks

### Parallel Opportunities

- **Setup**: 8 tasks can run in parallel (T002-T009 after T001)
- **Foundational**: Within each subsection (backend, frontend, docker), many tasks marked [P] can run in parallel
- **User Stories**: All 3 user stories (US1, US2, US3) can run completely in parallel once Foundational completes
- **Polish**: 9 tasks can run in parallel (T059-T062, T064-T066, T068-T069)

---

## Parallel Example: Foundational Phase (Backend)

```bash
# After T011 completes, launch these in parallel:
Task T012: "Create backend/src/config.py with Pydantic BaseSettings"
Task T015: "Create backend/src/models/__init__.py"
Task T018: "Create backend/src/middleware/__init__.py"
Task T020: "Create backend/src/services/__init__.py"
Task T022: "Create backend/src/api/__init__.py"

# After T016 (Task model) completes, launch:
Task T017: "Create Alembic migration for tasks table"
Task T021: "Create backend/src/services/task_service.py" (uses Task model)

# After T021 (service) completes, launch:
Task T024: "Create backend/src/api/tasks.py" (uses task_service)
```

---

## Parallel Example: User Stories (After Foundational Complete)

```bash
# All three user stories can start simultaneously:

# Developer A works on User Story 1:
Task T039-T048: "Infrastructure validation and documentation"

# Developer B works on User Story 2:
Task T049-T053: "Agent configuration validation"

# Developer C works on User Story 3:
Task T054-T058: "Phase tracking and documentation"

# All three complete independently and can be tested independently
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T009) - 9 tasks
2. Complete Phase 2: Foundational (T010-T038) - 29 tasks (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (T039-T048) - 10 tasks
4. **STOP and VALIDATE**: Test User Story 1 independently
   - Run docker-compose up
   - Run alembic upgrade head
   - Verify health endpoint
   - Verify frontend loads
   - Validate all documentation
5. Deploy/demo if ready - **48 tasks total for MVP**

### Incremental Delivery

1. **Foundation** (Phases 1-2): 38 tasks → Infrastructure ready
2. **+User Story 1** (Phase 3): +10 tasks = 48 total → Test independently → Deploy/Demo (MVP!)
3. **+User Story 2** (Phase 4): +5 tasks = 53 total → Test independently → Deploy/Demo
4. **+User Story 3** (Phase 5): +5 tasks = 58 total → Test independently → Deploy/Demo
5. **+Polish** (Phase 6): +12 tasks = 70 total → Final validation → Production deploy

Each story adds value without breaking previous stories.

### Parallel Team Strategy

With multiple developers:

1. **All developers together** complete Setup + Foundational (Phases 1-2) - 38 tasks
2. **Once Foundational is done**, split into parallel work:
   - **Developer A**: User Story 1 (T039-T048) - Infrastructure validation
   - **Developer B**: User Story 2 (T049-T053) - Agent configuration
   - **Developer C**: User Story 3 (T054-T058) - Phase tracking
3. **Reconvene** for Phase 6 (Polish) - shared quality tasks
4. Stories complete and integrate independently

---

## Task Summary

**Total Tasks**: 70 tasks

**Tasks by Phase**:
- Phase 1 (Setup): 9 tasks
- Phase 2 (Foundational): 29 tasks (BLOCKING)
- Phase 3 (User Story 1 - P1): 10 tasks
- Phase 4 (User Story 2 - P1): 5 tasks
- Phase 5 (User Story 3 - P2): 5 tasks
- Phase 6 (Polish): 12 tasks

**Tasks by User Story**:
- User Story 1: 10 tasks (infrastructure validation and documentation)
- User Story 2: 5 tasks (agent configuration validation)
- User Story 3: 5 tasks (phase tracking and documentation)
- Shared infrastructure: 38 tasks (Setup + Foundational)
- Cross-cutting: 12 tasks (Polish)

**Parallel Opportunities**:
- 37 tasks marked [P] can run in parallel (within phase constraints)
- 3 user stories can run completely in parallel after Foundational phase

**MVP Scope** (suggested):
- Phases 1-3 only (Setup + Foundational + User Story 1)
- 48 tasks total
- Delivers: Operational infrastructure, documented monorepo, agent configuration, phase tracking foundation

**Independent Test Criteria**:
- **User Story 1**: Docker Compose starts, migrations run, health endpoint responds, frontend loads, documentation complete
- **User Story 2**: All 4 agents defined in config with correct roles and models
- **User Story 3**: Phase tracking visible in config, README created, overview.md has success criteria

---

## Notes

- [P] tasks = different files, no dependencies on other tasks
- [Story] label (US1, US2, US3) maps task to specific user story for traceability
- Each user story is independently completable and testable
- Commit after each task or logical group of [P] tasks
- Stop at any checkpoint to validate story independently
- No tests requested in specification - implementation and validation only
- Foundational phase (Phase 2) is CRITICAL PATH - blocks all user story work
- User stories have NO dependencies on each other - maximum parallelization possible after foundation
