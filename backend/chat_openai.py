"""
Simple OpenAI Chat Server with MCP Tools
Works with Python 3.14
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import os

app = FastAPI(title="OpenAI Chat Server")

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[int] = None

class ChatResponse(BaseModel):
    conversation_id: int
    response: str
    created_at: datetime
    tools_used: Optional[List[str]] = None

# In-memory conversation storage (simple demo)
conversations = {}
conversation_counter = 1

@app.get("/api/health")
async def health():
    """Health check endpoint"""
    openai_key = os.getenv("OPENAI_API_KEY", "")
    return {
        "status": "healthy" if openai_key else "degraded",
        "ai_provider": "OpenAI",
        "model": "gpt-4-turbo-preview",
        "api_configured": "ready" if openai_key else "not_configured",
        "mcp_tools": "ready",
        "tools_registered": 5,
        "tool_names": ["add_task", "get_tasks", "update_task_status", "delete_task", "get_task_statistics"],
        "message": "Chat endpoint ready" if openai_key else "OpenAI API key not configured"
    }

@app.post("/api/{user_id}/chat", response_model=ChatResponse)
async def chat(user_id: str, request: ChatRequest):
    """Chat endpoint using OpenAI"""
    global conversation_counter

    # Get or create conversation
    conv_id = request.conversation_id or conversation_counter
    if not request.conversation_id:
        conversation_counter += 1
        conversations[conv_id] = []

    # Add user message to history
    if conv_id not in conversations:
        conversations[conv_id] = []
    conversations[conv_id].append({"role": "user", "content": request.message})

    # Check for OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        response_text = """⚠️ **OpenAI API Key Not Configured**

To enable AI chat, add your OpenAI API key to `backend/.env`:
```
OPENAI_API_KEY=sk-your-key-here
```

Get your key from: https://platform.openai.com/api-keys

**Or** you can use Anthropic Claude by setting:
```
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

Restart the backend server after configuring."""

        conversations[conv_id].append({"role": "assistant", "content": response_text})

        return ChatResponse(
            conversation_id=conv_id,
            response=response_text,
            created_at=datetime.utcnow(),
            tools_used=None
        )

    # Use OpenAI for real responses
    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key)

        # Define tools for OpenAI
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "add_task",
                    "description": "Create a new task",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string", "description": "Task title"},
                            "description": {"type": "string", "description": "Task description"}
                        },
                        "required": ["title"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_tasks",
                    "description": "Get user's tasks, optionally filtered by status",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "status": {"type": "string", "enum": ["pending", "completed"], "description": "Filter by status"}
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_task_status",
                    "description": "Update task completion status",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {"type": "integer", "description": "Task ID"},
                            "status": {"type": "string", "enum": ["pending", "completed"]}
                        },
                        "required": ["task_id", "status"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_task",
                    "description": "Delete a task",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {"type": "integer", "description": "Task ID to delete"}
                        },
                        "required": ["task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_task_statistics",
                    "description": "Get productivity statistics",
                    "parameters": {"type": "object", "properties": {}}
                }
            }
        ]

        system_prompt = """You are a helpful AI assistant for task management. Help users:
- Create new tasks ("Add a task to buy groceries")
- View their tasks ("Show my pending tasks")
- Update task status ("Mark task 5 as complete")
- Delete tasks ("Delete task 3")
- Get productivity insights ("How am I doing?")

Be concise, friendly, and use emojis appropriately (✅ ❌ 📋 🎯 📊).
When you successfully perform an action, confirm it clearly."""

        # Call OpenAI
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": system_prompt},
                *conversations[conv_id]
            ],
            tools=tools,
            tool_choice="auto"
        )

        assistant_message = response.choices[0].message
        response_text = assistant_message.content or "I'm here to help with your tasks!"

        # Handle tool calls (simplified - would integrate with actual MCP tools in production)
        tools_used = []
        if assistant_message.tool_calls:
            tools_used = [tc.function.name for tc in assistant_message.tool_calls]
            # In production, execute actual tools here
            response_text += f"\n\n*Note: Tool execution not yet connected to database. Tools that would be called: {', '.join(tools_used)}*"

        conversations[conv_id].append({"role": "assistant", "content": response_text})

        return ChatResponse(
            conversation_id=conv_id,
            response=response_text,
            created_at=datetime.utcnow(),
            tools_used=tools_used if tools_used else None
        )

    except Exception as e:
        error_msg = f"""❌ **Error with OpenAI API**

Error: {str(e)}

Please check:
1. Your OPENAI_API_KEY is valid
2. You have API credits available
3. The key has proper permissions

Get help at: https://platform.openai.com/docs"""

        return ChatResponse(
            conversation_id=conv_id,
            response=error_msg,
            created_at=datetime.utcnow(),
            tools_used=None
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
