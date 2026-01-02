"""Unit tests for CLI validators and interface functions."""

import pytest
from src.cli.validators import (
    validate_description,
    validate_task_id,
    validate_menu_choice,
)
from src.models.task import InvalidDescriptionError, InvalidInputError


class TestValidateDescription:
    """Tests for validate_description() function."""

    def test_valid_description(self):
        """Test validating a normal description."""
        result = validate_description("Buy groceries")

        assert result == "Buy groceries"

    def test_valid_description_with_whitespace(self):
        """Test that leading/trailing whitespace is stripped."""
        result = validate_description("  Buy groceries  ")

        assert result == "Buy groceries"

    def test_empty_description_raises_error(self):
        """Test that empty description raises InvalidDescriptionError."""
        with pytest.raises(InvalidDescriptionError, match="empty"):
            validate_description("")

    def test_whitespace_only_description_raises_error(self):
        """Test that whitespace-only description raises error."""
        with pytest.raises(InvalidDescriptionError, match="empty"):
            validate_description("   ")

    def test_description_with_tabs_and_newlines_raises_error_if_empty_after_strip(
        self,
    ):
        """Test that description with only tabs/newlines raises error."""
        with pytest.raises(InvalidDescriptionError, match="empty"):
            validate_description("\t\n  ")

    def test_description_at_max_length(self):
        """Test description at exactly 200 characters."""
        description = "x" * 200
        result = validate_description(description)

        assert result == description

    def test_description_exceeds_max_length_raises_error(self):
        """Test that description over 200 characters raises error."""
        description = "x" * 201
        with pytest.raises(InvalidDescriptionError, match="too long"):
            validate_description(description)

    def test_description_with_special_characters(self):
        """Test description with special characters is valid."""
        description = "Buy groceries! (milk, eggs, bread) & vegetables"
        result = validate_description(description)

        assert result == description

    def test_description_with_unicode_characters(self):
        """Test description with unicode characters is valid."""
        description = "Acheter du café ☕"
        result = validate_description(description)

        assert result == description

    def test_non_string_description_raises_error(self):
        """Test that non-string description raises InvalidDescriptionError."""
        with pytest.raises(InvalidDescriptionError, match="must be a string"):
            validate_description(123)  # type: ignore

    @pytest.mark.parametrize(
        "description",
        [
            "Buy groceries",
            "Write report for Q4",
            "Call dentist at 3pm",
            "x",  # Single character
            "a" * 200,  # Max length
        ],
    )
    def test_various_valid_descriptions(self, description):
        """Test various valid descriptions are accepted."""
        result = validate_description(description)

        assert result == description.strip()


class TestValidateTaskId:
    """Tests for validate_task_id() function."""

    def test_valid_task_id(self):
        """Test validating a valid task ID."""
        result = validate_task_id("1")

        assert result == 1

    def test_valid_multi_digit_task_id(self):
        """Test validating multi-digit task ID."""
        result = validate_task_id("123")

        assert result == 123

    def test_non_integer_input_raises_error(self):
        """Test that non-integer input raises InvalidInputError."""
        with pytest.raises(InvalidInputError, match="must be a number"):
            validate_task_id("abc")

    def test_zero_task_id_raises_error(self):
        """Test that task ID of 0 raises InvalidInputError."""
        with pytest.raises(InvalidInputError, match="positive number"):
            validate_task_id("0")

    def test_negative_task_id_raises_error(self):
        """Test that negative task ID raises InvalidInputError."""
        with pytest.raises(InvalidInputError, match="positive number"):
            validate_task_id("-5")

    def test_float_input_raises_error(self):
        """Test that float input raises InvalidInputError."""
        with pytest.raises(InvalidInputError, match="must be a number"):
            validate_task_id("1.5")

    def test_empty_string_raises_error(self):
        """Test that empty string raises InvalidInputError."""
        with pytest.raises(InvalidInputError, match="must be a number"):
            validate_task_id("")

    def test_whitespace_input_raises_error(self):
        """Test that whitespace input raises InvalidInputError."""
        with pytest.raises(InvalidInputError, match="must be a number"):
            validate_task_id("   ")

    @pytest.mark.parametrize("id_str,expected", [("1", 1), ("10", 10), ("999", 999)])
    def test_various_valid_task_ids(self, id_str, expected):
        """Test various valid task ID strings."""
        result = validate_task_id(id_str)

        assert result == expected


class TestValidateMenuChoice:
    """Tests for validate_menu_choice() function."""

    def test_valid_menu_choice(self):
        """Test validating a valid menu choice."""
        result = validate_menu_choice("3", 1, 6)

        assert result == 3

    def test_choice_at_min_boundary(self):
        """Test choice at minimum boundary."""
        result = validate_menu_choice("1", 1, 6)

        assert result == 1

    def test_choice_at_max_boundary(self):
        """Test choice at maximum boundary."""
        result = validate_menu_choice("6", 1, 6)

        assert result == 6

    def test_choice_below_min_raises_error(self):
        """Test that choice below minimum raises InvalidInputError."""
        with pytest.raises(InvalidInputError, match="between 1 and 6"):
            validate_menu_choice("0", 1, 6)

    def test_choice_above_max_raises_error(self):
        """Test that choice above maximum raises InvalidInputError."""
        with pytest.raises(InvalidInputError, match="between 1 and 6"):
            validate_menu_choice("7", 1, 6)

    def test_non_integer_choice_raises_error(self):
        """Test that non-integer choice raises InvalidInputError."""
        with pytest.raises(InvalidInputError, match="between"):
            validate_menu_choice("abc", 1, 6)

    def test_float_choice_raises_error(self):
        """Test that float choice raises InvalidInputError."""
        with pytest.raises(InvalidInputError, match="between"):
            validate_menu_choice("3.5", 1, 6)

    def test_empty_choice_raises_error(self):
        """Test that empty choice raises InvalidInputError."""
        with pytest.raises(InvalidInputError, match="between"):
            validate_menu_choice("", 1, 6)

    @pytest.mark.parametrize(
        "choice,min_val,max_val,expected",
        [
            ("1", 1, 6, 1),
            ("3", 1, 6, 3),
            ("6", 1, 6, 6),
            ("5", 1, 10, 5),
        ],
    )
    def test_various_valid_menu_choices(self, choice, min_val, max_val, expected):
        """Test various valid menu choices."""
        result = validate_menu_choice(choice, min_val, max_val)

        assert result == expected
