"""
MCP Tools Package - Model Context Protocol Tool Definitions

This package contains tool implementations for the Claude AI agent to interact
with the task management system.

Tools:
- add_task: Create a new task from natural language
- get_tasks: Retrieve tasks filtered by status
- update_task_status: Mark tasks as complete or pending
- delete_task: Remove tasks
- get_task_statistics: Get productivity insights
"""

from typing import List, Dict, Any

# Tool registry (populated at startup)
_tool_registry: List[Dict[str, Any]] = []


def register_tools():
    """
    Register all MCP tools for use with Claude AI.

    This function should be called at application startup to initialize
    the tool registry.
    """
    from .task_tools import get_all_tools

    global _tool_registry
    _tool_registry = get_all_tools()

    return _tool_registry


def get_registered_tools() -> List[Dict[str, Any]]:
    """
    Get all registered MCP tools.

    Returns:
        List of tool definitions compatible with Anthropic's tool use format
    """
    return _tool_registry


__all__ = [
    'register_tools',
    'get_registered_tools',
]
