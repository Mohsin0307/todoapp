"""Task model and custom exceptions for the todo application."""

from dataclasses import dataclass
from typing import Optional


# Custom Exception Classes
class TaskNotFoundError(Exception):
    """Raised when a task with the specified ID does not exist."""

    pass


class InvalidDescriptionError(Exception):
    """Raised when task description validation fails."""

    pass


class InvalidInputError(Exception):
    """Raised for general input validation failures."""

    pass


@dataclass
class Task:
    """Represents a single todo item.

    Attributes:
        id: Unique sequential integer identifier (assigned by TaskManager)
        description: Task description (1-200 characters, non-empty)
        status: Current status ("pending" or "completed")

    Invariants:
        - id must be positive integer > 0
        - description must be non-empty string after stripping whitespace
        - description must be <= 200 characters
        - status must be one of {"pending", "completed"}
    """

    id: int
    description: str
    status: str = "pending"

    def __post_init__(self) -> None:
        """Validate task attributes after initialization.

        Raises:
            InvalidDescriptionError: If description is empty or exceeds 200 characters
            ValueError: If id is not positive or status is invalid
        """
        # Validate ID
        if not isinstance(self.id, int) or self.id <= 0:
            raise ValueError(f"Task ID must be a positive integer, got: {self.id}")

        # Validate description
        if not isinstance(self.description, str):
            raise InvalidDescriptionError("Description must be a string")

        stripped_desc = self.description.strip()
        if not stripped_desc:
            raise InvalidDescriptionError("Description cannot be empty or whitespace-only")

        if len(self.description) > 200:
            raise InvalidDescriptionError(
                f"Description too long (max 200 characters, got {len(self.description)})"
            )

        # Validate status
        valid_statuses = {"pending", "completed"}
        if self.status not in valid_statuses:
            raise ValueError(
                f"Status must be one of {valid_statuses}, got: {self.status}"
            )
