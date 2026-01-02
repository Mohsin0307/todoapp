"""Chat API endpoint for AI-powered task management using Claude."""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import os

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

async def get_claude_response(user_message: str) -> str:
    """
    Get response from Claude AI.

    This function uses the Anthropic SDK to communicate with Claude.
    Falls back to helpful messages if API key is not configured.
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key or api_key.startswith("sk-ant-api03-xxx"):
        # API key not configured - return setup instructions
        if any(word in user_message.lower() for word in ["add", "create", "new task"]):
            return """✅ I can help you create a task!

**To activate full Claude AI features:**

1. Get your Anthropic API key from: https://console.anthropic.com/settings/keys
2. Add it to `backend/.env`:
   ```
   ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
   ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
   ```
3. Restart the backend server

Once configured, I'll be able to help you manage tasks naturally using Claude's advanced AI!"""

        elif any(word in user_message.lower() for word in ["list", "show", "what", "tasks"]):
            return """📋 To view your tasks with Claude AI chat:

**Setup Required:**
- Add your Anthropic API key to `backend/.env`
- Run database migrations: `python -m alembic upgrade head`
- Restart the server

Claude will then help you manage tasks conversationally!"""

        elif "help" in user_message.lower():
            return """🤖 **Claude AI Todo Chatbot**

**Current Status:** Using placeholder responses (Claude API not configured)

**To Enable Full AI Features:**

1. **Get Anthropic API Key:**
   - Visit: https://console.anthropic.com/settings/keys
   - Create a new API key

2. **Configure Backend:**
   ```bash
   cd backend
   cp .env.example .env
   # Edit .env and add:
   ANTHROPIC_API_KEY=sk-ant-api03-your-actual-key
   ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Server:**
   ```bash
   python -m uvicorn main:app --reload --port 8000
   ```

**What You Can Do (After Setup):**
- "Add a task to buy groceries"
- "Show me my pending tasks"
- "Mark task 5 as complete"
- "What's my progress today?"
- Natural language task management!

**Database:** Also run migrations: `python -m alembic upgrade head`"""

        else:
            return f"""💬 Message received: "{user_message}"

⚠️ **Claude AI not yet active**

To enable conversational AI with Claude:
1. Add `ANTHROPIC_API_KEY` to `backend/.env`
2. Get key from: https://console.anthropic.com/settings/keys
3. Restart server

Type 'help' for full setup instructions."""

    # If API key is configured, use Claude
    try:
        from anthropic import Anthropic

        client = Anthropic(api_key=api_key)
        model = os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")
        max_tokens = int(os.getenv("ANTHROPIC_MAX_TOKENS", "2048"))

        # System prompt for task management
        system_prompt = """You are a helpful AI assistant for task management. You help users:
- Create new tasks from natural language descriptions
- View and filter their task lists
- Update task status (complete/pending)
- Delete tasks
- Get productivity insights and statistics

Be concise, friendly, and use emojis appropriately. When a user asks to create, view, update, or delete tasks, acknowledge their request and explain that the full MCP tool integration is in progress.

For now, provide helpful responses about what you'll be able to do once the system is fully integrated."""

        # Call Claude API
        message = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_message}
            ]
        )

        # Extract response text
        response_text = message.content[0].text
        return response_text

    except ImportError:
        return """❌ **Anthropic SDK not installed**

Run in backend directory:
```bash
pip install -r requirements.txt
```

Then restart the server."""

    except Exception as e:
        return f"""❌ **Error connecting to Claude API**

Error: {str(e)}

Please check:
1. Your `ANTHROPIC_API_KEY` is valid
2. You have API credits available
3. Your internet connection is working

Get help at: https://docs.anthropic.com/"""

@router.post("/{user_id}/chat", response_model=ChatResponse)
async def chat(
    user_id: str,
    request: ChatRequest
):
    """
    Process chat message and return Claude AI response.

    Args:
        user_id: User identifier
        request: Chat request with message and optional conversation_id

    Returns:
        ChatResponse with Claude's reply
    """
    # Simulate conversation ID (in full implementation, this comes from database)
    conversation_id = request.conversation_id or 1

    # Get response from Claude
    response_text = await get_claude_response(request.message)

    return ChatResponse(
        conversation_id=conversation_id,
        response=response_text,
        created_at=datetime.utcnow()
    )

@router.get("/health")
async def chat_health():
    """Health check for chat service."""
    anthropic_configured = bool(os.getenv("ANTHROPIC_API_KEY")) and not os.getenv("ANTHROPIC_API_KEY", "").startswith("sk-ant-api03-xxx")

    return {
        "status": "ok",
        "ai_provider": "Anthropic Claude",
        "model": os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022"),
        "api_configured": anthropic_configured,
        "message": "Chat endpoint ready" if anthropic_configured else "Chat endpoint ready (awaiting API key configuration)"
    }
