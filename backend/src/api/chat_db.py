"""
Chat API endpoint for AI-powered task management using OpenAI GPT - Database-Backed Version

Production-ready version with full database persistence and tool integration.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
import os
from slowapi import Limiter
from slowapi.util import get_remote_address

from src.database import get_session
from src.services.agent_service import AgentService
from mcp_tools.task_tools import get_all_tools

limiter = Limiter(key_func=get_remote_address)

router = APIRouter()


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str = Field(..., min_length=1, max_length=1000, description="User message")
    conversation_id: Optional[int] = Field(None, description="Existing conversation ID")


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    conversation_id: int
    response: str
    created_at: datetime
    tools_used: Optional[List[str]] = None


@router.post("/{user_id}/chat", response_model=ChatResponse, tags=["chat"])
@limiter.limit("30/minute")
async def chat(
    user_id: str,
    request: ChatRequest,
    http_request: Request,
    session: AsyncSession = Depends(get_session)
):
    """
    Process chat message and return OpenAI GPT response with function calling (database-backed).
    Rate limited to 30 requests per minute per IP address.
    """
    try:
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
        import logging
        logging.error(f"Chat endpoint error: user_id={user_id} | error={str(e)}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process chat message: {str(e)}"
        )


@router.get("/health", tags=["health"])
async def chat_health():
    """
    Enhanced health check for chat service.
    """
    checks = {
        "status": "healthy",
        "ai_provider": "OpenAI GPT",
        "model": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        "api_configured": "unknown",
        "mcp_tools": "unknown",
        "tools_registered": 0,
        "tool_names": [],
        "database": "enabled",
        "message": ""
    }

    # Check OpenAI API configuration
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key and api_key != "your-openai-api-key-here":
            checks["api_configured"] = "ready"
        else:
            checks["api_configured"] = "not_configured"
            checks["status"] = "degraded"
            checks["message"] = "OpenAI API key not configured"
    except Exception as e:
        checks["api_configured"] = "error"
        checks["status"] = "unhealthy"
        checks["message"] = f"API config error: {str(e)}"

    # Check MCP tools
    try:
        tools = get_all_tools()
        if tools and len(tools) == 5:
            checks["mcp_tools"] = "ready"
            checks["tools_registered"] = len(tools)
            checks["tool_names"] = [t["function"]["name"] for t in tools]
        else:
            checks["mcp_tools"] = "incomplete"
            checks["status"] = "degraded"
            checks["message"] = f"Expected 5 tools, found {len(tools)}"
    except Exception as e:
        checks["mcp_tools"] = "error"
        checks["status"] = "unhealthy"
        checks["message"] = f"Tool registration error: {str(e)}"

    if checks["status"] == "healthy":
        checks["message"] = "Chat endpoint with database persistence and function calling ready"

    return checks


@router.get("/tools", tags=["tools"])
async def list_tools():
    """List all available tools."""
    tools = get_all_tools()
    return {
        "count": len(tools),
        "tools": tools,
        "note": "Tools are executed with database persistence via OpenAI function calling"
    }
