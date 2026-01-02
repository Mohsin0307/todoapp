"""
Task Management Tools for Claude AI - Database-Backed Version

These tools allow the Claude AI agent to interact with the task management system
using Anthropic's tool use format with real database persistence.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from uuid import UUID
import logging

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlmodel import and_

from src.models.task import Task
from src.services.task_service import TaskService

# Configure logging for MCP tools
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def add_task_tool_db(
    session: AsyncSession,
    title: str,
    description: Optional[str] = None,
    user_id: str = "demo-user"
) -> Dict[str, Any]:
    """
    Add a new task for the user (database-backed).

    Args:
        session: Database session
        title: Task title (required)
        description: Optional task description
        user_id: User ID (from JWT token)

    Returns:
        Dict with task_id and confirmation message
    """
    logger.info(f"MCP Tool Called (DB): add_task | user_id={user_id} | title='{title}' | description='{description or 'None'}'")

    try:
        # Convert user_id string to UUID (handle "demo-user" special case)
        if user_id == "demo-user":
            # Use a fixed UUID for demo user
            user_uuid = UUID("00000000-0000-0000-0000-000000000001")
        else:
            user_uuid = UUID(user_id)

        # Create task using TaskService
        task = await TaskService.create_task(
            session=session,
            user_id=user_uuid,
            title=title,
            description=description
        )

        # Commit the transaction
        await session.commit()

        result = {
            "success": True,
            "task_id": str(task.id),  # Convert UUID to string
            "title": task.title,
            "description": task.description or "",
            "status": "pending" if not task.completed else "completed",
            "created_at": task.created_at.isoformat(),
            "message": f"✅ Created task: {task.title}"
        }

        logger.info(f"MCP Tool Result (DB): add_task | success=True | task_id={result['task_id']}")
        return result

    except Exception as e:
        logger.error(f"MCP Tool Error (DB): add_task | error={str(e)}")
        await session.rollback()
        return {
            "success": False,
            "error": str(e),
            "message": f"❌ Failed to create task: {str(e)}"
        }


async def get_tasks_tool_db(
    session: AsyncSession,
    status: Optional[str] = None,
    user_id: str = "demo-user"
) -> Dict[str, Any]:
    """
    Get all tasks for the user, optionally filtered by status (database-backed).

    Args:
        session: Database session
        status: Filter by status ('pending' or 'completed'), None for all
        user_id: User ID (from JWT token)

    Returns:
        Dict with list of tasks
    """
    logger.info(f"MCP Tool Called (DB): get_tasks | user_id={user_id} | status_filter={status or 'all'}")

    try:
        # Convert user_id string to UUID
        if user_id == "demo-user":
            user_uuid = UUID("00000000-0000-0000-0000-000000000001")
        else:
            user_uuid = UUID(user_id)

        # Map status string to completed boolean
        completed_filter = None
        if status == "completed":
            completed_filter = True
        elif status == "pending":
            completed_filter = False

        # Get tasks using TaskService
        tasks = await TaskService.list_tasks(
            session=session,
            user_id=user_uuid,
            completed=completed_filter,
            limit=100
        )

        # Convert tasks to dict format
        task_list = []
        for task in tasks:
            task_dict = {
                "id": str(task.id),
                "title": task.title,
                "description": task.description or "",
                "status": "completed" if task.completed else "pending",
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat(),
            }
            if task.completed:
                task_dict["completed_at"] = task.updated_at.isoformat()
            task_list.append(task_dict)

        result = {
            "success": True,
            "tasks": task_list,
            "count": len(task_list),
            "filter": status or "all"
        }

        logger.info(f"MCP Tool Result (DB): get_tasks | success=True | count={result['count']} | filter={result['filter']}")
        return result

    except Exception as e:
        logger.error(f"MCP Tool Error (DB): get_tasks | error={str(e)}")
        return {
            "success": False,
            "error": str(e),
            "tasks": [],
            "count": 0,
            "message": f"❌ Failed to retrieve tasks: {str(e)}"
        }


async def update_task_status_tool_db(
    session: AsyncSession,
    task_id: str,
    status: str,
    user_id: str = "demo-user"
) -> Dict[str, Any]:
    """
    Update task status (complete or pending) - database-backed.

    Args:
        session: Database session
        task_id: ID of task to update (UUID string)
        status: New status ('completed' or 'pending')
        user_id: User ID (from JWT token)

    Returns:
        Dict with updated task info and confirmation
    """
    logger.info(f"MCP Tool Called (DB): update_task_status | user_id={user_id} | task_id={task_id} | new_status={status}")

    try:
        # Convert IDs to UUID
        if user_id == "demo-user":
            user_uuid = UUID("00000000-0000-0000-0000-000000000001")
        else:
            user_uuid = UUID(user_id)

        task_uuid = UUID(task_id)

        # Get the task first to know old status
        task = await TaskService.get_task(session, task_uuid, user_uuid)
        old_status = "completed" if task.completed else "pending"

        # Update task
        completed = (status == "completed")
        updated_task = await TaskService.update_task(
            session=session,
            task_id=task_uuid,
            user_id=user_uuid,
            completed=completed
        )

        # Commit the transaction
        await session.commit()

        result = {
            "success": True,
            "task_id": task_id,
            "title": updated_task.title,
            "old_status": old_status,
            "new_status": status,
            "message": f"✅ Marked '{updated_task.title}' as {status}"
        }

        logger.info(f"MCP Tool Result (DB): update_task_status | success=True | task_id={task_id} | status_changed={old_status}→{status}")
        return result

    except Exception as e:
        logger.error(f"MCP Tool Error (DB): update_task_status | error={str(e)}")
        await session.rollback()
        return {
            "success": False,
            "error": str(e),
            "message": f"❌ Failed to update task status: {str(e)}"
        }


async def delete_task_tool_db(
    session: AsyncSession,
    task_id: str,
    user_id: str = "demo-user"
) -> Dict[str, Any]:
    """
    Delete a task (soft delete) - database-backed.

    Args:
        session: Database session
        task_id: ID of task to delete (UUID string)
        user_id: User ID (from JWT token)

    Returns:
        Dict with deletion confirmation
    """
    logger.info(f"MCP Tool Called (DB): delete_task | user_id={user_id} | task_id={task_id}")

    try:
        # Convert IDs to UUID
        if user_id == "demo-user":
            user_uuid = UUID("00000000-0000-0000-0000-000000000001")
        else:
            user_uuid = UUID(user_id)

        task_uuid = UUID(task_id)

        # Get task title before deleting
        task = await TaskService.get_task(session, task_uuid, user_uuid)
        task_title = task.title

        # Delete task (soft delete)
        await TaskService.delete_task(session, task_uuid, user_uuid)

        # Commit the transaction
        await session.commit()

        result = {
            "success": True,
            "task_id": task_id,
            "title": task_title,
            "message": f"🗑️ Deleted task: {task_title}"
        }

        logger.info(f"MCP Tool Result (DB): delete_task | success=True | task_id={task_id} | action=deleted")
        return result

    except Exception as e:
        logger.error(f"MCP Tool Error (DB): delete_task | error={str(e)}")
        await session.rollback()
        return {
            "success": False,
            "error": str(e),
            "message": f"❌ Failed to delete task: {str(e)}"
        }


async def get_task_statistics_tool_db(
    session: AsyncSession,
    user_id: str = "demo-user"
) -> Dict[str, Any]:
    """
    Get productivity statistics and insights - database-backed.

    Args:
        session: Database session
        user_id: User ID (from JWT token)

    Returns:
        Dict with statistics about tasks
    """
    logger.info(f"MCP Tool Called (DB): get_task_statistics | user_id={user_id}")

    try:
        # Convert user_id to UUID
        if user_id == "demo-user":
            user_uuid = UUID("00000000-0000-0000-0000-000000000001")
        else:
            user_uuid = UUID(user_id)

        # Get all tasks
        all_tasks = await TaskService.list_tasks(session, user_uuid, limit=1000)

        # Calculate statistics
        total_tasks = len(all_tasks)
        completed_tasks = sum(1 for t in all_tasks if t.completed)
        pending_tasks = total_tasks - completed_tasks
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0.0

        # Get today's tasks
        today = datetime.utcnow().date()
        tasks_created_today = sum(1 for t in all_tasks if t.created_at.date() == today)
        tasks_completed_today = sum(
            1 for t in all_tasks
            if t.completed and t.updated_at.date() == today
        )

        # Calculate streak (simplified - just check if any tasks completed today)
        streak_days = 1 if tasks_completed_today > 0 else 0

        result = {
            "success": True,
            "statistics": {
                "total_tasks": total_tasks,
                "pending_tasks": pending_tasks,
                "completed_tasks": completed_tasks,
                "completion_rate": round(completion_rate, 1),
                "tasks_created_today": tasks_created_today,
                "tasks_completed_today": tasks_completed_today,
                "streak_days": streak_days
            },
            "message": f"📊 You have {pending_tasks} pending tasks and have completed {completed_tasks} ({round(completion_rate, 1)}% completion rate)"
        }

        logger.info(f"MCP Tool Result (DB): get_task_statistics | success=True | completion_rate={result['statistics']['completion_rate']}% | total={result['statistics']['total_tasks']}")
        return result

    except Exception as e:
        logger.error(f"MCP Tool Error (DB): get_task_statistics | error={str(e)}")
        return {
            "success": False,
            "error": str(e),
            "message": f"❌ Failed to get statistics: {str(e)}"
        }


def get_all_tools() -> List[Dict[str, Any]]:
    """
    Get all task tools in Anthropic's tool use format.

    Returns:
        List of tool definitions compatible with Claude
    """
    return [
        {
            "name": "add_task",
            "description": "Create a new task with a title and optional description",
            "input_schema": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "The task title (required)"
                    },
                    "description": {
                        "type": "string",
                        "description": "Optional task description or details"
                    }
                },
                "required": ["title"]
            }
        },
        {
            "name": "get_tasks",
            "description": "Get all tasks, optionally filtered by status (pending or completed)",
            "input_schema": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "enum": ["pending", "completed"],
                        "description": "Filter tasks by status. Omit to get all tasks."
                    }
                },
                "required": []
            }
        },
        {
            "name": "update_task_status",
            "description": "Update a task's status to completed or pending",
            "input_schema": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "The UUID of the task to update"
                    },
                    "status": {
                        "type": "string",
                        "enum": ["completed", "pending"],
                        "description": "The new status for the task"
                    }
                },
                "required": ["task_id", "status"]
            }
        },
        {
            "name": "delete_task",
            "description": "Permanently delete a task",
            "input_schema": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "The UUID of the task to delete"
                    }
                },
                "required": ["task_id"]
            }
        },
        {
            "name": "get_task_statistics",
            "description": "Get productivity statistics including total tasks, completion rate, and daily progress",
            "input_schema": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    ]


# Tool handler mapping for execution (async version)
TOOL_HANDLERS_DB = {
    "add_task": add_task_tool_db,
    "get_tasks": get_tasks_tool_db,
    "update_task_status": update_task_status_tool_db,
    "delete_task": delete_task_tool_db,
    "get_task_statistics": get_task_statistics_tool_db
}


async def execute_tool_db(
    session: AsyncSession,
    tool_name: str,
    tool_input: Dict[str, Any],
    user_id: str = "demo-user"
) -> Dict[str, Any]:
    """
    Execute a tool by name with given input (database-backed).

    Args:
        session: Database session
        tool_name: Name of the tool to execute
        tool_input: Input parameters for the tool
        user_id: User ID for scoping

    Returns:
        Tool execution result

    Raises:
        ValueError: If tool_name is not recognized
    """
    if tool_name not in TOOL_HANDLERS_DB:
        raise ValueError(f"Unknown tool: {tool_name}")

    handler = TOOL_HANDLERS_DB[tool_name]

    # Add session and user_id to all tool calls
    tool_input_with_context = {**tool_input, "session": session, "user_id": user_id}

    try:
        result = await handler(**tool_input_with_context)
        return result
    except Exception as e:
        logger.error(f"Tool execution failed: {tool_name} | error={str(e)}")
        return {
            "success": False,
            "error": str(e),
            "message": f"❌ Error executing {tool_name}: {str(e)}"
        }
