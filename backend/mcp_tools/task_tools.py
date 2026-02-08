"""
Task Management Tools for AI Chatbot

These tools allow the AI agent to interact with the task management system
using OpenAI's function calling format.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def add_task_tool(title: str, description: Optional[str] = None, user_id: str = "demo-user") -> Dict[str, Any]:
    """Add a new task for the user."""
    logger.info(f"MCP Tool Called: add_task | user_id={user_id} | title='{title}'")
    result = {
        "success": True,
        "task_id": 999,
        "title": title,
        "description": description or "",
        "status": "pending",
        "message": f"Created task: {title}"
    }
    return result


def get_tasks_tool(status: Optional[str] = None, user_id: str = "demo-user") -> Dict[str, Any]:
    """Get all tasks for the user, optionally filtered by status."""
    logger.info(f"MCP Tool Called: get_tasks | user_id={user_id} | status_filter={status or 'all'}")
    placeholder_tasks = [
        {"id": 1, "title": "Buy groceries", "description": "Milk, eggs, bread", "status": "pending"},
        {"id": 2, "title": "Call dentist", "description": "", "status": "pending"},
        {"id": 3, "title": "Finish report", "description": "Q4 financial report", "status": "completed"},
    ]
    if status:
        filtered_tasks = [t for t in placeholder_tasks if t["status"] == status]
    else:
        filtered_tasks = placeholder_tasks

    return {"success": True, "tasks": filtered_tasks, "count": len(filtered_tasks), "filter": status or "all"}


def update_task_status_tool(task_id: int, status: str, user_id: str = "demo-user") -> Dict[str, Any]:
    """Update task status (complete or pending)."""
    logger.info(f"MCP Tool Called: update_task_status | task_id={task_id} | new_status={status}")
    return {"success": True, "task_id": task_id, "new_status": status, "message": f"Marked task #{task_id} as {status}"}


def delete_task_tool(task_id: int, user_id: str = "demo-user") -> Dict[str, Any]:
    """Delete a task."""
    logger.info(f"MCP Tool Called: delete_task | task_id={task_id}")
    return {"success": True, "task_id": task_id, "message": f"Deleted task #{task_id}"}


def get_task_statistics_tool(user_id: str = "demo-user") -> Dict[str, Any]:
    """Get productivity statistics and insights."""
    logger.info(f"MCP Tool Called: get_task_statistics | user_id={user_id}")
    return {
        "success": True,
        "statistics": {
            "total_tasks": 10, "pending_tasks": 7, "completed_tasks": 3,
            "completion_rate": 30.0, "tasks_created_today": 2, "tasks_completed_today": 1,
        },
        "message": "You have 7 pending tasks and have completed 3 (30% completion rate)"
    }


def get_all_tools() -> List[Dict[str, Any]]:
    """
    Get all task tools in OpenAI function calling format.

    Returns:
        List of tool definitions compatible with OpenAI API
    """
    return [
        {
            "type": "function",
            "function": {
                "name": "add_task",
                "description": "Create a new task with a title and optional description",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string", "description": "The task title (required)"},
                        "description": {"type": "string", "description": "Optional task description or details"}
                    },
                    "required": ["title"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_tasks",
                "description": "Get all tasks, optionally filtered by status (pending or completed)",
                "parameters": {
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
            }
        },
        {
            "type": "function",
            "function": {
                "name": "update_task_status",
                "description": "Update a task's status to completed or pending",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "string", "description": "The UUID of the task to update"},
                        "status": {
                            "type": "string",
                            "enum": ["completed", "pending"],
                            "description": "The new status for the task"
                        }
                    },
                    "required": ["task_id", "status"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "delete_task",
                "description": "Permanently delete a task",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "string", "description": "The UUID of the task to delete"}
                    },
                    "required": ["task_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_task_statistics",
                "description": "Get productivity statistics including total tasks, completion rate, and daily progress",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        }
    ]


# Tool handler mapping for execution
TOOL_HANDLERS = {
    "add_task": add_task_tool,
    "get_tasks": get_tasks_tool,
    "update_task_status": update_task_status_tool,
    "delete_task": delete_task_tool,
    "get_task_statistics": get_task_statistics_tool
}


def execute_tool(tool_name: str, tool_input: Dict[str, Any], user_id: str = "demo-user") -> Dict[str, Any]:
    """Execute a tool by name with given input."""
    if tool_name not in TOOL_HANDLERS:
        raise ValueError(f"Unknown tool: {tool_name}")

    handler = TOOL_HANDLERS[tool_name]
    tool_input_with_user = {**tool_input, "user_id": user_id}

    try:
        return handler(**tool_input_with_user)
    except Exception as e:
        logger.error(f"Tool execution failed: {tool_name} | error={str(e)}")
        return {"success": False, "error": str(e), "message": f"Error executing {tool_name}: {str(e)}"}
