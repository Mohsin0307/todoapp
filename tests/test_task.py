"""Unit tests for Task dataclass and validation."""

import pytest
from src.models.task import Task, InvalidDescriptionError


class TestTaskCreation:
    """Tests for Task dataclass creation and validation."""

    def test_task_creation_with_valid_data(self):
        """Test creating a task with valid data."""
        task = Task(id=1, description="Buy groceries", status="pending")

        assert task.id == 1
        assert task.description == "Buy groceries"
        assert task.status == "pending"

    def test_task_creation_with_default_status(self):
        """Test that status defaults to 'pending'."""
        task = Task(id=1, description="Buy groceries")

        assert task.status == "pending"

    def test_task_creation_with_completed_status(self):
        """Test creating a task with 'completed' status."""
        task = Task(id=1, description="Buy groceries", status="completed")

        assert task.status == "completed"


class TestTaskValidation:
    """Tests for Task validation in __post_init__."""

    def test_invalid_task_id_zero(self):
        """Test that task ID of 0 raises ValueError."""
        with pytest.raises(ValueError, match="positive integer"):
            Task(id=0, description="Buy groceries")

    def test_invalid_task_id_negative(self):
        """Test that negative task ID raises ValueError."""
        with pytest.raises(ValueError, match="positive integer"):
            Task(id=-1, description="Buy groceries")

    def test_invalid_task_id_non_integer(self):
        """Test that non-integer ID raises ValueError."""
        with pytest.raises(ValueError):
            Task(id="1", description="Buy groceries")  # type: ignore

    def test_empty_description_raises_error(self):
        """Test that empty description raises InvalidDescriptionError."""
        with pytest.raises(InvalidDescriptionError, match="empty"):
            Task(id=1, description="")

    def test_whitespace_only_description_raises_error(self):
        """Test that whitespace-only description raises InvalidDescriptionError."""
        with pytest.raises(InvalidDescriptionError, match="empty"):
            Task(id=1, description="   ")

    def test_description_too_long_raises_error(self):
        """Test that description over 200 characters raises InvalidDescriptionError."""
        long_description = "x" * 201
        with pytest.raises(InvalidDescriptionError, match="too long"):
            Task(id=1, description=long_description)

    def test_description_exactly_200_chars_valid(self):
        """Test that description of exactly 200 characters is valid."""
        description = "x" * 200
        task = Task(id=1, description=description)

        assert task.description == description

    def test_invalid_status_raises_error(self):
        """Test that invalid status raises ValueError."""
        with pytest.raises(ValueError, match="Status must be one of"):
            Task(id=1, description="Buy groceries", status="invalid")

    @pytest.mark.parametrize("status", ["pending", "completed"])
    def test_valid_statuses(self, status):
        """Test that both valid statuses are accepted."""
        task = Task(id=1, description="Buy groceries", status=status)

        assert task.status == status

    def test_non_string_description_raises_error(self):
        """Test that non-string description raises InvalidDescriptionError."""
        with pytest.raises(InvalidDescriptionError, match="must be a string"):
            Task(id=1, description=123)  # type: ignore


class TestTaskRepresentation:
    """Tests for Task string representation and dataclass features."""

    def test_task_repr(self):
        """Test that Task has a useful repr."""
        task = Task(id=1, description="Buy groceries", status="pending")

        repr_str = repr(task)
        assert "Task" in repr_str
        assert "id=1" in repr_str
        assert "Buy groceries" in repr_str

    def test_task_equality(self):
        """Test that two tasks with same data are equal."""
        task1 = Task(id=1, description="Buy groceries", status="pending")
        task2 = Task(id=1, description="Buy groceries", status="pending")

        assert task1 == task2

    def test_task_inequality(self):
        """Test that tasks with different data are not equal."""
        task1 = Task(id=1, description="Buy groceries", status="pending")
        task2 = Task(id=2, description="Buy groceries", status="pending")

        assert task1 != task2
