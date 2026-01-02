"""Command-line interface functions for the todo application."""

from typing import NoReturn
from ..managers.task_manager import TaskManager
from ..models.task import TaskNotFoundError, InvalidDescriptionError, InvalidInputError
from .validators import validate_description, validate_task_id, validate_menu_choice


def display_menu() -> None:
    """Display the main menu options."""
    print("\n" + "=" * 40)
    print("         TODO LIST APPLICATION")
    print("=" * 40)
    print("\n1. Add a new task")
    print("2. View all tasks")
    print("3. Mark task as complete")
    print("4. Update task description")
    print("5. Delete a task")
    print("6. Exit")
    print()


def get_menu_choice() -> int:
    """Prompt user for menu selection and validate input.

    Returns:
        Valid menu choice (1-6)

    Note:
        Loops until valid input is received
    """
    while True:
        try:
            choice_input = input("Enter your choice (1-6): ")
            choice = validate_menu_choice(choice_input, 1, 6)
            return choice
        except InvalidInputError as e:
            print(f"\n✗ Error: {e}\n")


def view_tasks_flow(manager: TaskManager) -> None:
    """Execute view tasks workflow.

    Displays all tasks in a formatted table or shows empty list message.

    Args:
        manager: TaskManager instance
    """
    tasks = manager.get_all_tasks()

    print("\nYour Tasks:")
    print("=" * 80)

    if not tasks:
        print("No tasks found. Start by adding a task!")
    else:
        # Display header
        print(f"{'ID':<5} | {'Description':<50} | {'Status':<10}")
        print("-" * 5 + "-+-" + "-" * 50 + "-+-" + "-" * 10)

        # Display each task
        for task in tasks:
            # Truncate description if longer than 50 chars
            desc = task.description[:47] + "..." if len(task.description) > 50 else task.description
            print(f"{task.id:<5} | {desc:<50} | {task.status:<10}")

        print("=" * 80)
        print(f"Total tasks: {len(tasks)}")

    print()


def add_task_flow(manager: TaskManager) -> None:
    """Execute add task workflow.

    Prompts for description, validates input, creates task, and displays success message.

    Args:
        manager: TaskManager instance
    """
    try:
        description = input("\nEnter task description: ")
        task = manager.add_task(description)
        print(f"\n✓ Task added successfully (ID: {task.id})\n")
    except InvalidDescriptionError as e:
        print(f"\n✗ Error: {e}\n")


def mark_complete_flow(manager: TaskManager) -> None:
    """Execute mark complete workflow.

    Prompts for task ID, validates input, marks task complete, and displays result.

    Args:
        manager: TaskManager instance
    """
    try:
        id_input = input("\nEnter task ID to mark complete: ")
        task_id = validate_task_id(id_input)
        task = manager.mark_complete(task_id)
        print(f"\n✓ Task {task_id} marked as completed\n")
    except InvalidInputError as e:
        print(f"\n✗ Error: {e}\n")
    except TaskNotFoundError as e:
        print(f"\n✗ Error: {e}\n")


def update_task_flow(manager: TaskManager) -> None:
    """Execute update task workflow.

    Prompts for task ID and new description, validates input, updates task, and displays result.

    Args:
        manager: TaskManager instance
    """
    try:
        id_input = input("\nEnter task ID to update: ")
        task_id = validate_task_id(id_input)

        new_description = input("Enter new description: ")
        task = manager.update_task(task_id, new_description)
        print(f"\n✓ Task {task_id} updated successfully\n")
    except InvalidInputError as e:
        print(f"\n✗ Error: {e}\n")
    except TaskNotFoundError as e:
        print(f"\n✗ Error: {e}\n")
    except InvalidDescriptionError as e:
        print(f"\n✗ Error: {e}\n")


def delete_task_flow(manager: TaskManager) -> None:
    """Execute delete task workflow.

    Prompts for task ID, validates input, deletes task, and displays result.

    Args:
        manager: TaskManager instance
    """
    try:
        id_input = input("\nEnter task ID to delete: ")
        task_id = validate_task_id(id_input)
        manager.delete_task(task_id)
        print(f"\n✓ Task {task_id} deleted successfully\n")
    except InvalidInputError as e:
        print(f"\n✗ Error: {e}\n")
    except TaskNotFoundError as e:
        print(f"\n✗ Error: {e}\n")


def run_application() -> NoReturn:
    """Main application loop.

    Displays welcome message, initializes TaskManager, runs main menu loop,
    and displays goodbye message on exit.
    """
    # Display welcome message
    print("\n" + "=" * 40)
    print("    Welcome to TODO List Application")
    print("=" * 40)
    print("Track your tasks easily!")
    print()

    # Initialize task manager
    manager = TaskManager()

    # Main application loop
    while True:
        display_menu()
        choice = get_menu_choice()

        if choice == 1:
            add_task_flow(manager)
        elif choice == 2:
            view_tasks_flow(manager)
        elif choice == 3:
            mark_complete_flow(manager)
        elif choice == 4:
            update_task_flow(manager)
        elif choice == 5:
            delete_task_flow(manager)
        elif choice == 6:
            # Display goodbye message and exit
            print("\n" + "=" * 40)
            print("         Goodbye!")
            print("=" * 40)
            print("Your tasks will not be saved.")
            print("Thank you for using TODO List Application.")
            print()
            break
