"""Input validation functions for the CLI interface."""

from ..models.task import InvalidDescriptionError, InvalidInputError


def validate_description(description: str) -> str:
    """Validate and sanitize task description.

    Args:
        description: Raw user input for task description

    Returns:
        Stripped and validated description

    Raises:
        InvalidDescriptionError: If description is empty, whitespace-only, or exceeds 200 characters
    """
    if not isinstance(description, str):
        raise InvalidDescriptionError("Description must be a string")

    stripped = description.strip()

    if not stripped:
        raise InvalidDescriptionError("Description cannot be empty or whitespace-only")

    if len(description) > 200:
        raise InvalidDescriptionError(
            f"Description too long (max 200 characters, got {len(description)})"
        )

    return stripped


def validate_task_id(id_input: str) -> int:
    """Validate and parse task ID from user input.

    Args:
        id_input: Raw user input expected to be an integer string

    Returns:
        Parsed integer task ID

    Raises:
        InvalidInputError: If input is not a valid positive integer
    """
    try:
        task_id = int(id_input)
    except ValueError:
        raise InvalidInputError(f"Task ID must be a number, got: '{id_input}'")

    if task_id <= 0:
        raise InvalidInputError(f"Task ID must be a positive number, got: {task_id}")

    return task_id


def validate_menu_choice(choice_input: str, min_choice: int, max_choice: int) -> int:
    """Validate menu selection is within valid range.

    Args:
        choice_input: Raw user input for menu choice
        min_choice: Minimum valid choice (inclusive)
        max_choice: Maximum valid choice (inclusive)

    Returns:
        Parsed integer menu choice

    Raises:
        InvalidInputError: If input is not an integer or is out of range
    """
    try:
        choice = int(choice_input)
    except ValueError:
        raise InvalidInputError(
            f"Please enter a number between {min_choice} and {max_choice}"
        )

    if choice < min_choice or choice > max_choice:
        raise InvalidInputError(
            f"Please enter a number between {min_choice} and {max_choice}"
        )

    return choice
