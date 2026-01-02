"""
Chat API endpoint for AI-powered task management using Claude - Database-Backed Version

This is the production-ready version with full database persistence and tool integration.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
import os

from src.database import get_session
from src.services.agent_service import AgentService
from mcp_tools.task_tools import get_all_tools

router = APIRouter()


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str = Field(..., min_length=1, max_length=1000, description="User message")
    conversation_id: Optional[int] = Field(None, description="Existing conversation ID (None for new conversation)")


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    conversation_id: int
    response: str
    created_at: datetime
    tools_used: Optional[List[str]] = None


@router.post("/{user_id}/chat", response_model=ChatResponse, tags=["chat"])
async def chat(
    user_id: str,
    request: ChatRequest,
    session: AsyncSession = Depends(get_session)
):
    """
    Process chat message and return Claude AI response with tool execution (database-backed).

    This endpoint:
    1. Creates or retrieves a conversation
    2. Loads conversation history (last 50 messages)
    3. Sends message + history to Claude AI with tools
    4. Executes any tools Claude decides to use
    5. Persists user message and assistant response
    6. Returns response with conversation_id

    Args:
        user_id: User identifier
        request: Chat request with message and optional conversation_id
        session: Database session (injected)

    Returns:
        ChatResponse with Claude's reply, conversation_id, and tools used

    Raises:
        HTTPException: 500 if agent service fails
    """
    try:
        # Call agent service with database session
        response_text, conversation_id, tools_used = await AgentService.get_agent_response(
            session=session,
            user_id=user_id,
            user_message=request.message,
            conversation_id=request.conversation_id
        )

        return ChatResponse(
            conversation_id=conversation_id,
            response=response_text,
            created_at=datetime.utcnow(),
            tools_used=tools_used if tools_used else None
        )

    except Exception as e:
        # Log error and return 500
        import logging
        logging.error(f"Chat endpoint error: user_id={user_id} | error={str(e)}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process chat message: {str(e)}"
        )


@router.get("/health", tags=["health"])
async def chat_health():
    """
    Enhanced health check for chat service with database integration.

    Validates:
    - Claude AI configuration
    - MCP tools registration
    - Overall system status
    """
    checks = {
        "status": "healthy",
        "ai_provider": "Anthropic Claude",
        "model": os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022"),
        "api_configured": "unknown",
        "mcp_tools": "unknown",
        "tools_registered": 0,
        "tool_names": [],
        "database": "enabled",
        "message": ""
    }

    # Check Claude API configuration
    try:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if api_key and not api_key.startswith("sk-ant-api03-xxx"):
            checks["api_configured"] = "ready"
        else:
            checks["api_configured"] = "not_configured"
            checks["status"] = "degraded"
            checks["message"] = "Claude API key not configured"
    except Exception as e:
        checks["api_configured"] = "error"
        checks["status"] = "unhealthy"
        checks["message"] = f"API config error: {str(e)}"

    # Check MCP tools
    try:
        tools = get_all_tools()
        if tools and len(tools) == 5:  # Expected 5 tools
            checks["mcp_tools"] = "ready"
            checks["tools_registered"] = len(tools)
            checks["tool_names"] = [t["name"] for t in tools]
        else:
            checks["mcp_tools"] = "incomplete"
            checks["status"] = "degraded"
            checks["message"] = f"Expected 5 tools, found {len(tools)}"
    except Exception as e:
        checks["mcp_tools"] = "error"
        checks["status"] = "unhealthy"
        checks["message"] = f"Tool registration error: {str(e)}"

    # Set final message if healthy
    if checks["status"] == "healthy":
        checks["message"] = "Chat endpoint with database persistence and tool use ready"
    elif checks["status"] == "degraded":
        checks["message"] = checks.get("message", "Service partially operational")

    return checks


@router.get("/tools", tags=["tools"])
async def list_tools():
    """List all available MCP tools."""
    tools = get_all_tools()
    return {
        "count": len(tools),
        "tools": tools,
        "note": "Tools are executed with database persistence"
    }
