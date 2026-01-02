"""
Chat API with Claude Tool Integration - Phase III

Enhanced chat endpoint with MCP tool support for task management.
Works in standalone mode without database dependencies (uses placeholder data).
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import MCP tools
from mcp_tools.task_tools import get_all_tools, execute_tool

# Create FastAPI application
app = FastAPI(
    title="Todo AI Chat API with Tools",
    description="AI-Powered Task Management Chat with Claude Tool Use",
    version="3.0.0-tools",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


async def get_claude_response_with_tools(user_message: str, user_id: str = "demo-user") -> tuple[str, List[str]]:
    """
    Get response from Claude AI with tool use capability.

    Args:
        user_message: User's message
        user_id: User identifier

    Returns:
        Tuple of (response_text, tools_used)
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key or api_key.startswith("sk-ant-api03-xxx"):
        # API key not configured - return helpful setup message
        if any(word in user_message.lower() for word in ["add", "create", "new task"]):
            return ("""✅ I can help you create tasks!

**To activate Claude AI with tool capabilities:**

1. Get your Anthropic API key from: https://console.anthropic.com/settings/keys
2. Add it to `backend/.env`:
   ```
   ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
   ```
3. Restart the server

Once configured, I'll be able to actually create, update, and manage your tasks!""", [])

        elif "help" in user_message.lower():
            return ("""🤖 **Claude AI Todo Chatbot with Tools**

**Status**: Running in demo mode (Claude API not configured)

**What I can do (once API key is added)**:
- ✅ Create tasks: "Add a task to buy groceries"
- ✅ View tasks: "Show my pending tasks"
- ✅ Update tasks: "Mark buy groceries as done"
- ✅ Delete tasks: "Delete the groceries task"
- ✅ Get stats: "How am I doing today?"

**Available Tools**:
1. add_task - Create new tasks
2. get_tasks - View your task list
3. update_task_status - Mark tasks complete/pending
4. delete_task - Remove tasks
5. get_task_statistics - View productivity insights

**Setup**: Add ANTHROPIC_API_KEY to backend/.env and restart server.""", [])

        else:
            return (f'💬 Message received: "{user_message}"\n\n⚠️ Claude API not configured. Add ANTHROPIC_API_KEY to backend/.env to enable AI features. Type "help" for more info.', [])

    # Claude API is configured - use tool calling
    try:
        from anthropic import Anthropic

        # Create client with just API key (avoid proxy/http client issues)
        client = Anthropic(
            api_key=api_key,
            default_headers={}
        )
        model = os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")
        max_tokens = int(os.getenv("ANTHROPIC_MAX_TOKENS", "2048"))

        # Get available tools
        tools = get_all_tools()

        # System prompt for task management
        system_prompt = """You are a helpful AI assistant for task management. You help users:
- Create new tasks from natural language descriptions
- View and filter their task lists
- Update task status (complete/pending)
- Delete tasks
- Get productivity insights and statistics

You have access to these tools:
1. add_task(title, description?) - Create a new task
2. get_tasks(status?) - Get tasks (filter by 'pending' or 'completed')
3. update_task_status(task_id, status) - Update task status
4. delete_task(task_id) - Delete a task
5. get_task_statistics() - Get productivity stats

Be concise, friendly, and use emojis appropriately. When users ask about tasks, use the appropriate tools to retrieve or modify data. Always confirm actions and provide helpful feedback.

NOTE: This is running with placeholder data (database disabled). In production, these tools will perform real database operations."""

        # Track tools used
        tools_used = []

        # Call Claude API with tool support
        messages = [{"role": "user", "content": user_message}]

        response = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            system=system_prompt,
            tools=tools,
            messages=messages
        )

        # Process tool calls if any
        while response.stop_reason == "tool_use":
            # Extract tool use
            tool_use_block = None
            for block in response.content:
                if block.type == "tool_use":
                    tool_use_block = block
                    break

            if not tool_use_block:
                break

            tool_name = tool_use_block.name
            tool_input = tool_use_block.input
            tools_used.append(tool_name)

            print(f"Tool called: {tool_name} with input: {tool_input}")

            # Execute the tool
            tool_result = execute_tool(tool_name, tool_input, user_id)

            # Add assistant's tool use and tool result to conversation
            messages.append({
                "role": "assistant",
                "content": response.content
            })
            messages.append({
                "role": "user",
                "content": [{
                    "type": "tool_result",
                    "tool_use_id": tool_use_block.id,
                    "content": json.dumps(tool_result)
                }]
            })

            # Continue the conversation
            response = client.messages.create(
                model=model,
                max_tokens=max_tokens,
                system=system_prompt,
                tools=tools,
                messages=messages
            )

        # Extract final text response
        response_text = ""
        for block in response.content:
            if hasattr(block, "text"):
                response_text += block.text

        return (response_text, tools_used)

    except ImportError as e:
        return (f"❌ **Anthropic SDK not installed**\n\nError: {str(e)}\n\nRun: `pip install anthropic==0.39.0`\n\nThen restart the server.", [])

    except TypeError as e:
        # Specific handling for client initialization errors
        import traceback
        error_details = traceback.format_exc()
        return (f"❌ **Client Initialization Error**\n\nError: {str(e)}\n\nThis may be a version compatibility issue. Try:\n`pip install --upgrade anthropic httpx`\n\nDetails: {error_details[:200]}", [])

    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return (f"❌ **Error connecting to Claude API**\n\nError: {str(e)}\n\nStack: {error_details[:300]}", [])


@app.get("/")
async def root() -> dict[str, Any]:
    """Root endpoint - API information."""
    tools = get_all_tools()
    return {
        "name": "Todo AI Chat API with Tools",
        "version": "3.0.0-tools",
        "status": "operational (tool-enabled mode)",
        "docs": "/docs",
        "tools_available": len(tools),
        "tool_names": [t["name"] for t in tools],
        "note": "Claude AI with MCP tool support (placeholder data mode)"
    }


@app.post("/api/{user_id}/chat", response_model=ChatResponse)
async def chat(
    user_id: str,
    request: ChatRequest
):
    """
    Process chat message and return Claude AI response with tool use.

    Args:
        user_id: User identifier
        request: Chat request with message

    Returns:
        ChatResponse with Claude's reply and tools used
    """
    # Simulate conversation ID
    conversation_id = request.conversation_id or 1

    # Get response from Claude with tools
    response_text, tools_used = await get_claude_response_with_tools(request.message, user_id)

    return ChatResponse(
        conversation_id=conversation_id,
        response=response_text,
        created_at=datetime.utcnow(),
        tools_used=tools_used if tools_used else None
    )


@app.get("/api/health")
async def chat_health():
    """
    Enhanced health check for chat service.

    Validates:
    - Claude AI configuration
    - MCP tools registration
    - Database connection (if applicable)
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
        checks["message"] = "Chat endpoint with tool use ready"
    elif checks["status"] == "degraded":
        checks["message"] = checks.get("message", "Service partially operational")

    return checks


@app.get("/api/tools")
async def list_tools():
    """List all available MCP tools."""
    tools = get_all_tools()
    return {
        "count": len(tools),
        "tools": tools
    }
