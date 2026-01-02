"""Unit tests for TaskManager class."""

import pytest
from src.managers.task_manager import TaskManager
from src.models.task import Task, TaskNotFoundError, InvalidDescriptionError


@pytest.fixture
def manager():
    """Create a fresh TaskManager instance for each test."""
    return TaskManager()


@pytest.fixture
def manager_with_tasks():
    """Create a TaskManager with some pre-populated tasks."""
    mgr = TaskManager()
    mgr.add_task("Buy groceries")
    mgr.add_task("Write report")
    mgr.add_task("Call dentist")
    return mgr


class TestTaskManagerAddTask:
    """Tests for TaskManager.add_task() method."""

    def test_add_task_with_valid_description(self, manager):
        """Test adding a task with valid description."""
        task = manager.add_task("Buy groceries")

        assert task.id == 1
        assert task.description == "Buy groceries"
        assert task.status == "pending"

    def test_add_task_returns_task_instance(self, manager):
        """Test that add_task returns a Task instance."""
        task = manager.add_task("Buy groceries")

        assert isinstance(task, Task)

    def test_add_task_sequential_id_generation(self, manager):
        """Test that task IDs are generated sequentially."""
        task1 = manager.add_task("Task 1")
        task2 = manager.add_task("Task 2")
        task3 = manager.add_task("Task 3")

        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3

    def test_add_task_with_empty_description_raises_error(self, manager):
        """Test that adding task with empty description raises InvalidDescriptionError."""
        with pytest.raises(InvalidDescriptionError):
            manager.add_task("")

    def test_add_task_with_whitespace_only_raises_error(self, manager):
        """Test that adding task with whitespace-only description raises error."""
        with pytest.raises(InvalidDescriptionError):
            manager.add_task("   ")

    def test_add_task_with_description_too_long_raises_error(self, manager):
        """Test that adding task with >200 char description raises error."""
        long_description = "x" * 201
        with pytest.raises(InvalidDescriptionError):
            manager.add_task(long_description)

    def test_add_task_strips_whitespace(self, manager):
        """Test that add_task strips leading/trailing whitespace from description."""
        task = manager.add_task("  Buy groceries  ")

        assert task.description == "Buy groceries"

    def test_add_multiple_tasks_increments_id(self, manager):
        """Test that adding multiple tasks increments ID correctly."""
        for i in range(1, 11):
            task = manager.add_task(f"Task {i}")
            assert task.id == i


class TestTaskManagerGetAllTasks:
    """Tests for TaskManager.get_all_tasks() method."""

    def test_get_all_tasks_returns_empty_list_initially(self, manager):
        """Test that get_all_tasks returns empty list for new manager."""
        tasks = manager.get_all_tasks()

        assert tasks == []
        assert len(tasks) == 0

    def test_get_all_tasks_returns_list_of_tasks(self, manager_with_tasks):
        """Test that get_all_tasks returns list of Task instances."""
        tasks = manager_with_tasks.get_all_tasks()

        assert len(tasks) == 3
        assert all(isinstance(task, Task) for task in tasks)

    def test_get_all_tasks_preserves_insertion_order(self, manager):
        """Test that get_all_tasks returns tasks in insertion order."""
        manager.add_task("First task")
        manager.add_task("Second task")
        manager.add_task("Third task")

        tasks = manager.get_all_tasks()

        assert tasks[0].description == "First task"
        assert tasks[1].description == "Second task"
        assert tasks[2].description == "Third task"

    def test_get_all_tasks_returns_copy_not_reference(self, manager):
        """Test that get_all_tasks returns a new list, not internal storage reference."""
        manager.add_task("Task 1")
        tasks1 = manager.get_all_tasks()
        tasks2 = manager.get_all_tasks()

        # Should be equal but not the same object
        assert tasks1 == tasks2
        assert tasks1 is not tasks2

    def test_get_all_tasks_after_adding_many(self, manager):
        """Test get_all_tasks with larger number of tasks."""
        for i in range(100):
            manager.add_task(f"Task {i}")

        tasks = manager.get_all_tasks()

        assert len(tasks) == 100
        assert tasks[0].id == 1
        assert tasks[99].id == 100


class TestTaskManagerGetTask:
    """Tests for TaskManager.get_task() method."""

    def test_get_task_by_id(self, manager_with_tasks):
        """Test retrieving a task by its ID."""
        task = manager_with_tasks.get_task(2)

        assert task.id == 2
        assert task.description == "Write report"

    def test_get_task_not_found_raises_error(self, manager):
        """Test that getting non-existent task raises TaskNotFoundError."""
        with pytest.raises(TaskNotFoundError):
            manager.get_task(999)

    def test_get_task_from_empty_manager_raises_error(self, manager):
        """Test that getting task from empty manager raises TaskNotFoundError."""
        with pytest.raises(TaskNotFoundError):
            manager.get_task(1)


class TestTaskManagerTaskCount:
    """Tests for TaskManager.task_count() method."""

    def test_task_count_zero_initially(self, manager):
        """Test that task_count returns 0 for new manager."""
        assert manager.task_count() == 0

    def test_task_count_after_adding_tasks(self, manager):
        """Test that task_count increments correctly."""
        assert manager.task_count() == 0

        manager.add_task("Task 1")
        assert manager.task_count() == 1

        manager.add_task("Task 2")
        assert manager.task_count() == 2

        manager.add_task("Task 3")
        assert manager.task_count() == 3

    def test_task_count_with_prepopulated_manager(self, manager_with_tasks):
        """Test task_count with pre-populated manager."""
        assert manager_with_tasks.task_count() == 3
