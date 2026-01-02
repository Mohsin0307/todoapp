"""Integration tests for end-to-end user scenarios."""

import pytest
from src.managers.task_manager import TaskManager
from src.models.task import Task


@pytest.fixture
def manager():
    """Create a fresh TaskManager for integration tests."""
    return TaskManager()


class TestAddAndViewScenario:
    """Integration tests for User Story 1: Add and View Tasks."""

    def test_add_single_task_and_view(self, manager):
        """Test adding a single task and viewing it."""
        # Add a task
        task = manager.add_task("Buy groceries")

        # Verify task was created correctly
        assert task.id == 1
        assert task.description == "Buy groceries"
        assert task.status == "pending"

        # View all tasks
        all_tasks = manager.get_all_tasks()

        assert len(all_tasks) == 1
        assert all_tasks[0].id == 1
        assert all_tasks[0].description == "Buy groceries"
        assert all_tasks[0].status == "pending"

    def test_add_multiple_tasks_and_view_all(self, manager):
        """Test adding multiple tasks and viewing them all."""
        # Add multiple tasks
        task1 = manager.add_task("Buy groceries")
        task2 = manager.add_task("Write report")
        task3 = manager.add_task("Call dentist")

        # Verify sequential IDs
        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3

        # View all tasks
        all_tasks = manager.get_all_tasks()

        # Verify all tasks are in the list
        assert len(all_tasks) == 3
        assert all_tasks[0].description == "Buy groceries"
        assert all_tasks[1].description == "Write report"
        assert all_tasks[2].description == "Call dentist"

    def test_view_empty_list_initially(self, manager):
        """Test viewing tasks when list is empty (acceptance scenario 4)."""
        all_tasks = manager.get_all_tasks()

        assert all_tasks == []
        assert len(all_tasks) == 0

    def test_add_task_with_empty_description_shows_error(self, manager):
        """Test that adding task with empty description raises error (acceptance scenario 3)."""
        from src.models.task import InvalidDescriptionError

        with pytest.raises(InvalidDescriptionError):
            manager.add_task("")

        # Verify no task was added
        assert manager.task_count() == 0

    def test_task_list_maintains_insertion_order(self, manager):
        """Test that viewing tasks shows them in insertion order."""
        # Add tasks in specific order
        manager.add_task("First")
        manager.add_task("Second")
        manager.add_task("Third")
        manager.add_task("Fourth")

        # Retrieve and verify order
        tasks = manager.get_all_tasks()

        assert tasks[0].description == "First"
        assert tasks[1].description == "Second"
        assert tasks[2].description == "Third"
        assert tasks[3].description == "Fourth"

    def test_add_and_view_with_whitespace_trimming(self, manager):
        """Test that descriptions with whitespace are trimmed when added."""
        task = manager.add_task("  Buy groceries  ")

        # Verify whitespace was stripped
        assert task.description == "Buy groceries"

        # Verify in list view
        all_tasks = manager.get_all_tasks()
        assert all_tasks[0].description == "Buy groceries"

    def test_add_task_with_long_description(self, manager):
        """Test adding task with maximum allowed description length."""
        long_description = "x" * 200

        task = manager.add_task(long_description)

        assert task.description == long_description
        assert len(task.description) == 200

    def test_add_task_with_special_characters(self, manager):
        """Test adding task with special characters in description."""
        description = "Buy groceries: milk, eggs, bread & butter (organic)"

        task = manager.add_task(description)

        assert task.description == description

        # Verify in list view
        tasks = manager.get_all_tasks()
        assert tasks[0].description == description

    def test_sequential_add_view_operations(self, manager):
        """Test performing add and view operations sequentially."""
        # Add first task and view
        manager.add_task("Task 1")
        assert len(manager.get_all_tasks()) == 1

        # Add second task and view
        manager.add_task("Task 2")
        assert len(manager.get_all_tasks()) == 2

        # Add third task and view
        manager.add_task("Task 3")
        tasks = manager.get_all_tasks()

        assert len(tasks) == 3
        assert tasks[0].id == 1
        assert tasks[1].id == 2
        assert tasks[2].id == 3

    def test_add_many_tasks_performance(self, manager):
        """Test that system can handle adding many tasks (success criterion SC-001)."""
        # Add 100 tasks
        for i in range(100):
            task = manager.add_task(f"Task {i}")
            assert task.id == i + 1

        # Verify all tasks can be viewed
        tasks = manager.get_all_tasks()

        assert len(tasks) == 100
        assert tasks[0].description == "Task 0"
        assert tasks[99].description == "Task 99"

    def test_all_tasks_have_default_pending_status(self, manager):
        """Test that all newly added tasks have 'pending' status."""
        manager.add_task("Task 1")
        manager.add_task("Task 2")
        manager.add_task("Task 3")

        tasks = manager.get_all_tasks()

        for task in tasks:
            assert task.status == "pending"

    def test_task_ids_are_unique_and_sequential(self, manager):
        """Test that task IDs are unique and sequential (FR-001)."""
        ids = []

        for i in range(20):
            task = manager.add_task(f"Task {i}")
            ids.append(task.id)

        # Verify all IDs are unique
        assert len(ids) == len(set(ids))

        # Verify IDs are sequential starting from 1
        assert ids == list(range(1, 21))


class TestMarkCompleteScenario:
    """Integration tests for User Story 2: Mark Tasks Complete."""

    def test_mark_pending_task_as_complete(self, manager):
        """Test marking a pending task changes status to 'completed' (acceptance scenario 1)."""
        # Add a task
        task = manager.add_task("Buy groceries")
        assert task.status == "pending"

        # Mark it complete
        completed_task = manager.mark_complete(task.id)

        # Verify status changed
        assert completed_task.status == "completed"
        assert completed_task.id == task.id
        assert completed_task.description == task.description

    def test_mark_non_existent_task_shows_error(self, manager):
        """Test marking non-existent task ID shows error (acceptance scenario 2)."""
        from src.models.task import TaskNotFoundError

        # Try to mark non-existent task complete
        with pytest.raises(TaskNotFoundError):
            manager.mark_complete(999)

    def test_completed_task_displays_in_list(self, manager):
        """Test completed task displays with 'completed' status in list (acceptance scenario 3)."""
        # Add and complete a task
        task1 = manager.add_task("Buy groceries")
        task2 = manager.add_task("Write report")
        manager.mark_complete(task1.id)

        # View all tasks
        tasks = manager.get_all_tasks()

        # Verify completed status shows correctly
        assert tasks[0].status == "completed"
        assert tasks[1].status == "pending"

    def test_mark_already_completed_task_is_idempotent(self, manager):
        """Test marking already-completed task handles gracefully (acceptance scenario 4)."""
        # Add and complete a task
        task = manager.add_task("Buy groceries")
        manager.mark_complete(task.id)

        # Mark it complete again
        task_again = manager.mark_complete(task.id)

        # Verify it's still completed, no error
        assert task_again.status == "completed"

    def test_mark_complete_workflow_end_to_end(self, manager):
        """Test complete workflow: add multiple tasks, mark some complete, view list."""
        # Add multiple tasks
        task1 = manager.add_task("Buy groceries")
        task2 = manager.add_task("Write report")
        task3 = manager.add_task("Call dentist")

        # Mark first and third complete
        manager.mark_complete(task1.id)
        manager.mark_complete(task3.id)

        # Get all tasks
        tasks = manager.get_all_tasks()

        # Verify statuses
        assert tasks[0].status == "completed"  # Buy groceries
        assert tasks[1].status == "pending"    # Write report
        assert tasks[2].status == "completed"  # Call dentist

    def test_mark_complete_preserves_description(self, manager):
        """Test that marking complete doesn't change task description."""
        task = manager.add_task("Important task with details")
        original_desc = task.description

        completed = manager.mark_complete(task.id)

        assert completed.description == original_desc


class TestUpdateDescriptionScenario:
    """Integration tests for User Story 3: Update Task Description."""

    def test_update_existing_task_description(self, manager):
        """Test updating task description changes it (acceptance scenario 1)."""
        # Add a task
        task = manager.add_task("Buy groceries")
        original_id = task.id

        # Update the description
        updated = manager.update_task(task.id, "Buy organic groceries")

        # Verify description changed
        assert updated.description == "Buy organic groceries"
        assert updated.id == original_id
        assert updated.status == "pending"

    def test_update_non_existent_task_shows_error(self, manager):
        """Test updating non-existent task ID shows error (acceptance scenario 2)."""
        from src.models.task import TaskNotFoundError

        with pytest.raises(TaskNotFoundError):
            manager.update_task(999, "New description")

    def test_update_with_empty_description_shows_error(self, manager):
        """Test updating with empty description shows error (acceptance scenario 3)."""
        from src.models.task import InvalidDescriptionError

        # Add a task
        task = manager.add_task("Buy groceries")

        # Try to update with empty description
        with pytest.raises(InvalidDescriptionError):
            manager.update_task(task.id, "")

    def test_updated_task_displays_in_list(self, manager):
        """Test updated task shows new description in list (acceptance scenario 4)."""
        # Add multiple tasks
        task1 = manager.add_task("Buy groceries")
        task2 = manager.add_task("Write report")

        # Update first task
        manager.update_task(task1.id, "Buy organic groceries")

        # View all tasks
        tasks = manager.get_all_tasks()

        # Verify updated description shows correctly
        assert tasks[0].description == "Buy organic groceries"
        assert tasks[1].description == "Write report"

    def test_update_preserves_status(self, manager):
        """Test that updating description preserves task status."""
        # Add and complete a task
        task = manager.add_task("Buy groceries")
        manager.mark_complete(task.id)

        # Update description
        updated = manager.update_task(task.id, "Buy organic groceries")

        # Verify status is still completed
        assert updated.status == "completed"
        assert updated.description == "Buy organic groceries"

    def test_update_with_whitespace_trimming(self, manager):
        """Test that updated descriptions with whitespace are trimmed."""
        task = manager.add_task("Original description")

        updated = manager.update_task(task.id, "  New description  ")

        # Verify whitespace was stripped
        assert updated.description == "New description"

    def test_update_workflow_end_to_end(self, manager):
        """Test complete workflow: add tasks, update some, view list."""
        # Add multiple tasks
        task1 = manager.add_task("Task 1")
        task2 = manager.add_task("Task 2")
        task3 = manager.add_task("Task 3")

        # Update tasks with different scenarios
        manager.update_task(task1.id, "Updated Task 1")
        manager.mark_complete(task2.id)
        manager.update_task(task2.id, "Updated Completed Task 2")

        # Get all tasks
        tasks = manager.get_all_tasks()

        # Verify updates
        assert tasks[0].description == "Updated Task 1"
        assert tasks[0].status == "pending"
        assert tasks[1].description == "Updated Completed Task 2"
        assert tasks[1].status == "completed"
        assert tasks[2].description == "Task 3"
        assert tasks[2].status == "pending"

    def test_update_preserves_task_id(self, manager):
        """Test that updating description doesn't change task ID."""
        task = manager.add_task("Original description")
        original_id = task.id

        # Update multiple times
        manager.update_task(task.id, "First update")
        manager.update_task(task.id, "Second update")
        updated = manager.update_task(task.id, "Third update")

        # Verify ID unchanged
        assert updated.id == original_id
        assert updated.description == "Third update"


class TestDeleteTaskScenario:
    """Integration tests for User Story 4: Delete Tasks."""

    def test_delete_existing_task(self, manager):
        """Test deleting a task removes it from the list (acceptance scenario 1)."""
        # Add tasks
        task1 = manager.add_task("Task 1")
        task2 = manager.add_task("Task 2")
        task3 = manager.add_task("Task 3")

        # Delete middle task
        manager.delete_task(task2.id)

        # Verify it's gone
        tasks = manager.get_all_tasks()
        assert len(tasks) == 2
        assert tasks[0].id == task1.id
        assert tasks[1].id == task3.id

    def test_delete_non_existent_task_shows_error(self, manager):
        """Test deleting non-existent task ID shows error (acceptance scenario 2)."""
        from src.models.task import TaskNotFoundError

        with pytest.raises(TaskNotFoundError):
            manager.delete_task(999)

    def test_deleted_task_not_in_list(self, manager):
        """Test deleted task does not appear in list (acceptance scenario 3)."""
        # Add tasks
        task1 = manager.add_task("Buy groceries")
        task2 = manager.add_task("Write report")

        # Delete first task
        manager.delete_task(task1.id)

        # Verify it's not in list
        tasks = manager.get_all_tasks()
        assert len(tasks) == 1
        assert tasks[0].id == task2.id
        assert tasks[0].description == "Write report"

    def test_delete_all_tasks_shows_empty_list(self, manager):
        """Test deleting all tasks shows empty list message (acceptance scenario 4)."""
        # Add tasks
        task1 = manager.add_task("Task 1")
        task2 = manager.add_task("Task 2")

        # Delete all tasks
        manager.delete_task(task1.id)
        manager.delete_task(task2.id)

        # Verify empty list
        tasks = manager.get_all_tasks()
        assert len(tasks) == 0
        assert tasks == []

    def test_delete_workflow_end_to_end(self, manager):
        """Test complete workflow: add tasks, delete some, view remaining."""
        # Add multiple tasks
        task1 = manager.add_task("Task 1")
        task2 = manager.add_task("Task 2")
        task3 = manager.add_task("Task 3")
        task4 = manager.add_task("Task 4")

        # Delete first and third tasks
        manager.delete_task(task1.id)
        manager.delete_task(task3.id)

        # Get remaining tasks
        tasks = manager.get_all_tasks()

        # Verify only task 2 and 4 remain
        assert len(tasks) == 2
        assert tasks[0].id == task2.id
        assert tasks[0].description == "Task 2"
        assert tasks[1].id == task4.id
        assert tasks[1].description == "Task 4"

    def test_delete_task_count_decreases(self, manager):
        """Test that task count decreases after deletion."""
        # Add tasks
        manager.add_task("Task 1")
        manager.add_task("Task 2")
        manager.add_task("Task 3")
        assert manager.task_count() == 3

        # Delete one task
        manager.delete_task(1)
        assert manager.task_count() == 2

        # Delete another
        manager.delete_task(2)
        assert manager.task_count() == 1

    def test_delete_completed_task(self, manager):
        """Test deleting a completed task works correctly."""
        # Add and complete a task
        task = manager.add_task("Completed task")
        manager.mark_complete(task.id)

        # Delete it
        manager.delete_task(task.id)

        # Verify it's gone
        tasks = manager.get_all_tasks()
        assert len(tasks) == 0

    def test_cannot_delete_same_task_twice(self, manager):
        """Test that deleting same task twice raises error."""
        from src.models.task import TaskNotFoundError

        # Add and delete task
        task = manager.add_task("Task")
        manager.delete_task(task.id)

        # Try to delete again
        with pytest.raises(TaskNotFoundError):
            manager.delete_task(task.id)
