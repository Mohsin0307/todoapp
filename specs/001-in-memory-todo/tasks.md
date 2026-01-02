# Tasks: In-Memory Todo Console Application

**Input**: Design documents from `/specs/001-in-memory-todo/`
**Prerequisites**: plan.md ✅, spec.md ✅, ADRs ✅ (0001-data-architecture, 0002-error-handling, 0003-multi-agent-workflow)

**Tests**: TDD approach with pytest - tests written FIRST, implementation SECOND

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

Single project structure at repository root:
- **Source**: `src/`
- **Tests**: `tests/`
- **Docs**: Root level (README.md, CLAUDE.md)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project directory structure (src/, tests/, src/models/, src/managers/, src/cli/)
- [X] T002 Initialize Python project with pyproject.toml (pytest dev dependency)
- [X] T003 [P] Create .gitignore for Python (__pycache__, .pytest_cache, .env, *.pyc)
- [X] T004 [P] Create src/__init__.py and all module __init__.py files
- [X] T005 [P] Create tests/__init__.py for test discovery

**Checkpoint**: Project structure ready for implementation

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T006 Define custom exception classes in src/models/task.py (TaskNotFoundError, InvalidDescriptionError, InvalidInputError)
- [X] T007 [P] Create Task dataclass with validation in src/models/task.py
- [X] T008 Create validators module in src/cli/validators.py (validate_description, validate_task_id, validate_menu_choice)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add and View Tasks (Priority: P1) 🎯 MVP

**Goal**: Enable users to add new tasks and view their task list - the core value proposition

**Independent Test**: Launch app, add tasks with descriptions, view the list. Delivers immediate value as a basic task tracker.

**Acceptance Criteria** (from spec.md):
1. Adding task "Buy groceries" stores it with unique ID and status "pending"
2. Viewing multiple tasks shows formatted list with ID, description, status
3. Adding task with empty description shows clear error message
4. Viewing tasks when none exist shows friendly empty message

### Tests for User Story 1 ⚠️ WRITE TESTS FIRST

> **TDD Mandate**: Write these tests FIRST, ensure they FAIL before implementation

- [X] T009 [P] [US1] Unit test for Task dataclass validation in tests/test_task.py (test_task_creation, test_invalid_description, test_status_default)
- [X] T010 [P] [US1] Unit test for TaskManager.add_task() in tests/test_task_manager.py (test_add_valid_task, test_add_empty_description, test_sequential_id_generation)
- [X] T011 [P] [US1] Unit test for TaskManager.get_all_tasks() in tests/test_task_manager.py (test_get_all_tasks_empty, test_get_all_tasks_multiple, test_insertion_order)
- [X] T012 [P] [US1] Unit test for validate_description() in tests/test_cli.py (test_valid_description, test_empty_description, test_whitespace_only, test_max_length)
- [X] T013 [P] [US1] Integration test for add and view flow in tests/test_integration.py (test_add_and_view_scenario, test_empty_list_display)

### Implementation for User Story 1

- [X] T014 [US1] Implement Task dataclass in src/models/task.py (id, description, status, __post_init__ validation)
- [X] T015 [US1] Implement TaskManager class in src/managers/task_manager.py (add_task, get_all_tasks, _tasks dict, _next_id counter)
- [X] T016 [US1] Implement validate_description() in src/cli/validators.py (strip, length check, non-empty check)
- [X] T017 [US1] Implement display_menu() in src/cli/interface.py (menu options 1-6 with formatting)
- [X] T018 [US1] Implement view_tasks_flow() in src/cli/interface.py (format task list, handle empty state)
- [X] T019 [US1] Implement add_task_flow() in src/cli/interface.py (prompt, validate, call manager, display success)
- [X] T020 [US1] Create main.py application entry point (welcome message, main loop, goodbye message)

**Checkpoint**: At this point, User Story 1 should be fully functional - users can add and view tasks independently

**Run Tests**: `pytest tests/test_task.py tests/test_task_manager.py tests/test_cli.py tests/test_integration.py -v`

---

## Phase 4: User Story 2 - Mark Tasks as Complete (Priority: P2)

**Goal**: Enable users to track progress by marking tasks complete

**Independent Test**: Add tasks (using P1 functionality), mark them complete, verify status changes. Delivers value as a progress tracker.

**Acceptance Criteria** (from spec.md):
1. Marking pending task changes status to "completed"
2. Marking non-existent task ID shows error message
3. Completed task displays with "completed" status in list
4. Marking already-completed task handles gracefully (idempotent)

### Tests for User Story 2 ⚠️ WRITE TESTS FIRST

- [X] T021 [P] [US2] Unit test for TaskManager.mark_complete() in tests/test_task_manager.py (test_mark_complete_valid, test_mark_complete_not_found, test_mark_complete_idempotent)
- [X] T022 [P] [US2] Unit test for validate_task_id() in tests/test_cli.py (test_valid_id, test_non_integer, test_negative_id, test_zero_id)
- [X] T023 [P] [US2] Integration test for mark complete flow in tests/test_integration.py (test_mark_complete_scenario, test_mark_complete_error_handling)

### Implementation for User Story 2

- [X] T024 [US2] Implement TaskManager.mark_complete() in src/managers/task_manager.py (find task, update status, return task)
- [X] T025 [US2] Implement TaskManager.get_task() in src/managers/task_manager.py (lookup by ID, raise TaskNotFoundError if missing)
- [X] T026 [US2] Implement validate_task_id() in src/cli/validators.py (parse integer, validate positive)
- [X] T027 [US2] Implement mark_complete_flow() in src/cli/interface.py (prompt ID, validate, call manager, display success/error)
- [X] T028 [US2] Integrate mark_complete_flow into main loop in src/main.py (menu choice 3)

**Checkpoint**: User Stories 1 AND 2 both work independently - basic task tracking with completion

**Run Tests**: `pytest tests/test_task_manager.py::test_mark_complete* tests/test_cli.py::test_validate_task_id* tests/test_integration.py::test_mark_complete* -v`

---

## Phase 5: User Story 3 - Update Task Description (Priority: P3)

**Goal**: Enable users to fix mistakes or clarify tasks without deleting and re-adding

**Independent Test**: Add tasks, update descriptions, verify changes persist. Delivers value as an error-correction tool.

**Acceptance Criteria** (from spec.md):
1. Updating task changes description successfully
2. Updating non-existent task ID shows error message
3. Updating with empty description shows error
4. Updated description displays correctly in task list

### Tests for User Story 3 ⚠️ WRITE TESTS FIRST

- [X] T029 [P] [US3] Unit test for TaskManager.update_task() in tests/test_task_manager.py (test_update_valid, test_update_not_found, test_update_empty_description)
- [X] T030 [P] [US3] Integration test for update flow in tests/test_integration.py (test_update_scenario, test_update_error_handling)

### Implementation for User Story 3

- [X] T031 [US3] Implement TaskManager.update_task() in src/managers/task_manager.py (find task, validate description, update, return task)
- [X] T032 [US3] Implement update_task_flow() in src/cli/interface.py (prompt ID, prompt new description, validate, call manager, display success/error)
- [X] T033 [US3] Integrate update_task_flow into main loop in src/main.py (menu choice 4)

**Checkpoint**: User Stories 1, 2, AND 3 all work independently - full task editing capability

**Run Tests**: `pytest tests/test_task_manager.py::test_update* tests/test_integration.py::test_update* -v`

---

## Phase 6: User Story 4 - Delete Tasks (Priority: P4)

**Goal**: Enable users to remove tasks and keep list clean

**Independent Test**: Add tasks, delete specific ones by ID, verify removal from list. Delivers value as a list maintenance tool.

**Acceptance Criteria** (from spec.md):
1. Deleting task removes it from list
2. Deleting non-existent task ID shows error message
3. Deleted task does not appear in task list
4. Deleting all tasks shows empty list message

### Tests for User Story 4 ⚠️ WRITE TESTS FIRST

- [X] T034 [P] [US4] Unit test for TaskManager.delete_task() in tests/test_task_manager.py (test_delete_valid, test_delete_not_found, test_delete_all_tasks)
- [X] T035 [P] [US4] Unit test for TaskManager.task_count() in tests/test_task_manager.py (test_task_count_empty, test_task_count_multiple)
- [X] T036 [P] [US4] Integration test for delete flow in tests/test_integration.py (test_delete_scenario, test_delete_all_shows_empty_message)

### Implementation for User Story 4

- [X] T037 [US4] Implement TaskManager.delete_task() in src/managers/task_manager.py (find task, remove from dict, raise if not found)
- [X] T038 [US4] Implement TaskManager.task_count() in src/managers/task_manager.py (return len of _tasks dict)
- [X] T039 [US4] Implement delete_task_flow() in src/cli/interface.py (prompt ID, validate, call manager, display success/error)
- [X] T040 [US4] Integrate delete_task_flow into main loop in src/main.py (menu choice 5)

**Checkpoint**: All user stories complete - full CRUD functionality operational

**Run Tests**: `pytest tests/test_task_manager.py::test_delete* tests/test_integration.py::test_delete* -v`

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and final validation

- [X] T041 [P] Create README.md with setup instructions, usage guide, examples
- [X] T042 [P] Add comprehensive docstrings to all public methods (TaskManager, validators, interface)
- [X] T043 [P] Add type hints to all function signatures (verify 100% coverage)
- [X] T044 [P] Implement get_menu_choice() with validation loop in src/cli/interface.py
- [X] T045 Implement validate_menu_choice() in src/cli/validators.py (validate range 1-6)
- [X] T046 Add error handling for all InvalidInputError cases in CLI flows
- [X] T047 Add welcome/goodbye message formatting in src/main.py
- [X] T048 [P] Performance test with 1000+ tasks in tests/test_integration.py (verify <100ms operations)
- [X] T049 [P] Edge case tests in tests/test_task.py (max int ID, 200 char description, rapid operations)
- [X] T050 Run full test suite with coverage report (`pytest --cov=src tests/ -v`)
- [X] T051 Validate PEP 8 compliance (run `ruff check src/ tests/` or `flake8`)
- [X] T052 Final integration test: Run all user scenarios from spec.md acceptance criteria
- [X] T053 Manual smoke test: Run application, execute all menu options, verify UI formatting

**Checkpoint**: Production-ready application with full documentation and test coverage

**Run All Tests**: `pytest tests/ -v --cov=src --cov-report=term-missing`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion (T001-T005) - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion (T006-T008)
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order: P1 → P2 → P3 → P4 (recommended for single developer)
- **Polish (Phase 7)**: Depends on all user stories being complete (T009-T040)

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Uses US1's TaskManager but independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Uses US1's TaskManager but independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Uses US1's TaskManager but independently testable

### Within Each User Story

**TDD Flow** (CRITICAL):
1. **Tests FIRST**: Write all test tasks for the story, run tests, verify they FAIL
2. **Implementation SECOND**: Write implementation tasks, run tests, verify they PASS
3. **Checkpoint**: Story complete when all tests pass

**Task Order**:
- Tests before implementation (TDD)
- Models before managers
- Managers before CLI interface
- CLI flows before main loop integration

### Parallel Opportunities

#### Setup Phase (T001-T005):
- T003, T004, T005 can run in parallel (independent files)

#### Foundational Phase (T006-T008):
- T007 and T008 can run in parallel after T006 completes (validators independent of Task)

#### User Story 1 Tests (T009-T013):
- ALL test tasks can run in parallel (different test files/functions)

#### User Story 1 Implementation (T014-T020):
- T016 can start immediately (validators independent)
- T014 must complete before T015 (TaskManager depends on Task)
- T017, T018, T019 depend on T015 (need TaskManager)
- T020 depends on T017-T019 (needs all flows)

#### User Story 2+ Tests:
- All test tasks within each story marked [P] can run in parallel

#### Cross-Story Parallelism (if multiple developers):
- After Foundational phase (T008), all 4 user stories (Phase 3-6) can proceed in parallel
- Developer A: US1 (T009-T020)
- Developer B: US2 (T021-T028)
- Developer C: US3 (T029-T033)
- Developer D: US4 (T034-T040)

#### Polish Phase (T041-T053):
- T041, T042, T043, T044, T048, T049, T051 can run in parallel (different files)

---

## Parallel Example: User Story 1

```bash
# Write all tests for User Story 1 in parallel:
Task T009: "Unit test for Task dataclass validation in tests/test_task.py"
Task T010: "Unit test for TaskManager.add_task() in tests/test_task_manager.py"
Task T011: "Unit test for TaskManager.get_all_tasks() in tests/test_task_manager.py"
Task T012: "Unit test for validate_description() in tests/test_cli.py"
Task T013: "Integration test for add and view flow in tests/test_integration.py"

# Run tests, verify they FAIL (no implementation yet)
pytest tests/ -v

# Implement in parallel (where possible):
Task T014: "Implement Task dataclass in src/models/task.py"
Task T016: "Implement validate_description() in src/cli/validators.py" [parallel with T014]

# Then sequential (dependencies):
Task T015: "Implement TaskManager" (needs Task from T014)
Task T017-T019: "Implement CLI flows" (need TaskManager from T015)
Task T020: "Create main.py" (needs all flows)

# Run tests again, verify they PASS
pytest tests/ -v
```

---

## Implementation Strategy

### MVP First (User Story 1 Only - Recommended Start)

1. Complete Phase 1: Setup (T001-T005)
2. Complete Phase 2: Foundational (T006-T008) - CRITICAL
3. Complete Phase 3: User Story 1 (T009-T020)
4. **STOP and VALIDATE**: Run `pytest tests/ -v`
5. **Manual Test**: Run `python src/main.py` and test add/view operations
6. **DECISION POINT**: Deploy basic task tracker or continue to next story?

**Value Delivered**: Working task tracker with add and view capabilities

### Incremental Delivery (Recommended)

1. **Foundation** (T001-T008) → Project structure ready ✅
2. **US1 Complete** (T009-T020) → Add & View works → Demo MVP! 🎯
3. **US2 Complete** (T021-T028) → Mark complete works → Demo progress tracking!
4. **US3 Complete** (T029-T033) → Update works → Demo editing!
5. **US4 Complete** (T034-T040) → Delete works → Demo full CRUD!
6. **Polish** (T041-T053) → Production ready → Final demo!

Each checkpoint delivers working, testable value without breaking previous stories.

### Parallel Team Strategy (If Multiple Developers)

With 4 developers:

1. **All together**: Complete Setup (Phase 1) + Foundational (Phase 2)
2. **Once Foundational done**, split:
   - **Developer A**: User Story 1 (T009-T020) - Tests first, then implementation
   - **Developer B**: User Story 2 (T021-T028) - Tests first, then implementation
   - **Developer C**: User Story 3 (T029-T033) - Tests first, then implementation
   - **Developer D**: User Story 4 (T034-T040) - Tests first, then implementation
3. **Integration**: Each developer tests their story independently
4. **All together**: Complete Polish phase (T041-T053)

**Timeline**: ~6-8 hours total with parallel execution vs ~11 hours sequential

---

## Task Summary

**Total Tasks**: 53
- **Setup**: 5 tasks (T001-T005)
- **Foundational**: 3 tasks (T006-T008)
- **User Story 1**: 12 tasks (T009-T020) - 5 tests, 7 implementation
- **User Story 2**: 8 tasks (T021-T028) - 3 tests, 5 implementation
- **User Story 3**: 5 tasks (T029-T033) - 2 tests, 3 implementation
- **User Story 4**: 7 tasks (T034-T040) - 3 tests, 4 implementation
- **Polish**: 13 tasks (T041-T053)

**Parallel Opportunities**: 23 tasks marked [P] can run in parallel (43% of all tasks)

**Independent Test Criteria**:
- US1: Launch app, add 3 tasks, view list → Success if all display correctly
- US2: Add task, mark complete, view list → Success if status changes to "completed"
- US3: Add task, update description, view list → Success if new description shows
- US4: Add 3 tasks, delete 1, view list → Success if only 2 tasks remain

**Suggested MVP Scope**: Phase 1 + Phase 2 + Phase 3 (US1 only) = 20 tasks = **Minimal viable task tracker**

---

## Success Metrics

### Test Coverage (Target: >80%)
- [ ] All public methods have unit tests
- [ ] All user scenarios from spec.md have integration tests
- [ ] All edge cases from spec.md have tests
- [ ] All tests passing: `pytest tests/ -v`

### Code Quality (Target: 100%)
- [ ] PEP 8 compliance: `ruff check src/ tests/` (zero violations)
- [ ] Type hints: All functions have type annotations
- [ ] Docstrings: All public methods documented

### Performance (Target: <100ms)
- [ ] Menu display: <50ms
- [ ] All CRUD operations: <100ms with 1000 tasks
- [ ] Application startup: <500ms

### Functional Completeness (Target: 100%)
- [ ] All 14 FR requirements from spec.md implemented
- [ ] All 4 user stories validated independently
- [ ] All 10 edge cases handled gracefully
- [ ] All success criteria (SC-001 to SC-007) met

### Constitution Compliance
- [ ] Spec-Driven Development: No manual code edits
- [ ] Phase Discipline: No future-phase features
- [ ] Documentation: README.md complete
- [ ] Code Quality: Production-ready standards
- [ ] Performance: <100ms operations, 1000+ task support

---

## Notes

- **[P] marker**: Tasks can run in parallel (different files, no dependencies)
- **[Story] label**: Maps task to specific user story for traceability (US1, US2, US3, US4)
- **TDD Mandate**: Tests MUST be written before implementation, verify FAIL, then implement, verify PASS
- **Independent Stories**: Each user story should be completable and testable without others
- **Commit Strategy**: Commit after completing each user story phase (checkpoint)
- **Validation**: Stop at each checkpoint to test story independently before continuing
- **File Conflicts**: Tasks operating on same file (e.g., multiple flows in interface.py) must run sequentially
- **Avoid**: Vague tasks, cross-story dependencies that break independence, implementing before testing

---

**Document Version**: 1.0
**Generated**: 2025-12-30
**Next Step**: Execute Phase 1 (Setup) tasks T001-T005
**Execution Mode**: TDD (Test-Driven Development) - Tests first, always
