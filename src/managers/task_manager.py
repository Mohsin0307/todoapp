"""TaskManager class for managing in-memory task storage and operations."""

from typing import List
from ..models.task import Task, TaskNotFoundError


class TaskManager:
    """Manages in-memory task storage and CRUD operations.

    Uses a dictionary for O(1) task lookup by ID and maintains an
    auto-incrementing counter for sequential ID generation.
    """

    def __init__(self) -> None:
        """Initialize TaskManager with empty task storage."""
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1

    def add_task(self, description: str) -> Task:
        """Add a new task with the given description.

        Args:
            description: Task description (1-200 chars, non-empty)

        Returns:
            Created Task instance with assigned ID and 'pending' status

        Raises:
            InvalidDescriptionError: If description is empty or >200 chars
        """
        # Sanitize description (trim whitespace)
        clean_description = description.strip()

        # Create new task with current ID (Task.__post_init__ will validate)
        task = Task(id=self._next_id, description=clean_description, status="pending")

        # Store task
        self._tasks[task.id] = task

        # Increment ID counter for next task
        self._next_id += 1

        return task

    def get_all_tasks(self) -> List[Task]:
        """Retrieve all tasks in insertion order.

        Returns:
            List of all Task instances (empty list if no tasks)
            Insertion order is preserved (Python 3.7+ dict behavior)
        """
        return list(self._tasks.values())

    def get_task(self, task_id: int) -> Task:
        """Retrieve a specific task by ID.

        Args:
            task_id: Task identifier

        Returns:
            Task instance with matching ID

        Raises:
            TaskNotFoundError: If task_id doesn't exist
        """
        if task_id not in self._tasks:
            raise TaskNotFoundError(f"Task with ID {task_id} not found")

        return self._tasks[task_id]

    def update_task(self, task_id: int, description: str) -> Task:
        """Update task description.

        Args:
            task_id: Task identifier
            description: New description (1-200 chars, non-empty)

        Returns:
            Updated Task instance

        Raises:
            TaskNotFoundError: If task_id doesn't exist
            InvalidDescriptionError: If description is invalid
        """
        # Get existing task (raises TaskNotFoundError if not found)
        task = self.get_task(task_id)

        # Sanitize new description (trim whitespace)
        clean_description = description.strip()

        # Create updated task (Task.__post_init__ will validate)
        updated_task = Task(
            id=task.id, description=clean_description, status=task.status
        )

        # Store updated task
        self._tasks[task_id] = updated_task

        return updated_task

    def delete_task(self, task_id: int) -> None:
        """Delete a task by ID.

        Args:
            task_id: Task identifier

        Raises:
            TaskNotFoundError: If task_id doesn't exist
        """
        if task_id not in self._tasks:
            raise TaskNotFoundError(f"Task with ID {task_id} not found")

        del self._tasks[task_id]

    def mark_complete(self, task_id: int) -> Task:
        """Mark a task as completed.

        Args:
            task_id: Task identifier

        Returns:
            Updated Task instance with status="completed"

        Raises:
            TaskNotFoundError: If task_id doesn't exist

        Note:
            Idempotent - marking an already completed task has no effect
        """
        # Get existing task (raises TaskNotFoundError if not found)
        task = self.get_task(task_id)

        # Create updated task with completed status
        updated_task = Task(id=task.id, description=task.description, status="completed")

        # Store updated task
        self._tasks[task_id] = updated_task

        return updated_task

    def task_count(self) -> int:
        """Get total number of tasks.

        Returns:
            Number of tasks in storage
        """
        return len(self._tasks)
