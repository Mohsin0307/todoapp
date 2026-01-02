"""
HACKATHON DEMO: AI-Powered Todo Chatbot
Simplified standalone version that works without database

This demonstrates the Phase III AI chatbot concept with placeholder data.
For production, use the full database-backed version with Python 3.11.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uvicorn

app = FastAPI(
    title="AI Todo Chatbot - Hackathon Demo",
    description="Demonstrates AI-powered task management with natural language",
    version="3.0.0-demo"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory task storage for demo
tasks_db = {}
conversation_id_counter = 1

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[int] = None

class ChatResponse(BaseModel):
    conversation_id: int
    response: str
    created_at: datetime
    tools_used: Optional[List[str]] = None

# Auth models for demo
class SignupRequest(BaseModel):
    name: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class AuthResponse(BaseModel):
    user: dict
    session: dict

def process_message(user_id: str, message: str) -> tuple[str, List[str]]:
    """Process user message and return response with tools used."""
    message_lower = message.lower()
    tools_used = []

    # Task Creation
    if any(word in message_lower for word in ["add", "create", "new task"]):
        # Extract task title (simple extraction)
        title = message.replace("add a task to", "").replace("create a task to", "").replace("add task", "").strip()
        if not title:
            title = "New Task"

        task_id = len(tasks_db.get(user_id, [])) + 1
        if user_id not in tasks_db:
            tasks_db[user_id] = []

        tasks_db[user_id].append({
            "id": task_id,
            "title": title.capitalize(),
            "status": "pending",
            "created_at": datetime.utcnow().isoformat()
        })

        tools_used.append("add_task")
        return f"✅ Created task #{task_id}: {title.capitalize()}", tools_used

    # List Tasks
    elif any(word in message_lower for word in ["list", "show", "what", "tasks", "pending"]):
        if user_id not in tasks_db or not tasks_db[user_id]:
            return "📋 You don't have any tasks yet. Try saying 'Add a task to buy groceries'", []

        tools_used.append("get_tasks")
        pending = [t for t in tasks_db[user_id] if t["status"] == "pending"]
        completed = [t for t in tasks_db[user_id] if t["status"] == "completed"]

        response = "📋 **Your Tasks:**\n\n"
        if pending:
            response += "**Pending:**\n"
            for t in pending:
                response += f"{t['id']}. {t['title']}\n"
        if completed:
            response += "\n**Completed:**\n"
            for t in completed:
                response += f"✓ {t['title']}\n"

        return response, tools_used

    # Complete Task
    elif any(word in message_lower for word in ["complete", "done", "finish", "mark"]):
        tools_used.append("update_task_status")

        # Try to extract task number
        words = message_lower.split()
        task_num = None
        for word in words:
            if word.isdigit():
                task_num = int(word)
                break

        if task_num and user_id in tasks_db:
            for task in tasks_db[user_id]:
                if task["id"] == task_num:
                    task["status"] = "completed"
                    return f"✅ Marked task #{task_num} '{task['title']}' as completed!", tools_used

        return "❌ Couldn't find that task. Try 'show my tasks' to see task numbers.", tools_used

    # Delete Task
    elif any(word in message_lower for word in ["delete", "remove"]):
        tools_used.append("delete_task")

        words = message_lower.split()
        task_num = None
        for word in words:
            if word.isdigit():
                task_num = int(word)
                break

        if task_num and user_id in tasks_db:
            tasks_db[user_id] = [t for t in tasks_db[user_id] if t["id"] != task_num]
            return f"🗑️ Deleted task #{task_num}", tools_used

        return "❌ Couldn't find that task to delete.", tools_used

    # Statistics
    elif any(word in message_lower for word in ["stats", "statistics", "progress", "how am i"]):
        tools_used.append("get_task_statistics")

        if user_id not in tasks_db or not tasks_db[user_id]:
            return "📊 No tasks yet! Start by adding some tasks.", tools_used

        total = len(tasks_db[user_id])
        completed = len([t for t in tasks_db[user_id] if t["status"] == "completed"])
        pending = total - completed
        completion_rate = (completed / total * 100) if total > 0 else 0

        return f"""📊 **Your Productivity Stats:**

Total Tasks: {total}
Completed: {completed}
Pending: {pending}
Completion Rate: {completion_rate:.1f}%

{"🎉 Great job!" if completion_rate > 50 else "💪 Keep going!"}""", tools_used

    # Help
    elif "help" in message_lower:
        return """🤖 **AI Todo Chatbot - Demo Mode**

**What I can do:**
✅ "Add a task to buy groceries"
✅ "Show my tasks"
✅ "Mark task 1 as done"
✅ "Delete task 2"
✅ "How am I doing?" (statistics)

**Note**: This is a simplified demo for the hackathon. The full version uses:
- Claude AI with tool calling
- PostgreSQL database
- Conversation history
- Advanced natural language understanding

**Tech Stack:**
- Backend: FastAPI + SQLModel
- AI: Anthropic Claude with MCP tools
- Frontend: Next.js + ChatKit (coming soon)""", []

    # Default
    else:
        return f"""💬 I understand you said: "{message}"

I can help you manage tasks! Try:
- "Add a task to [task name]"
- "Show my tasks"
- "Complete task [number]"
- "Delete task [number]"
- "How am I doing?"
- "help" for more info""", []

@app.get("/")
def root():
    return {
        "name": "AI Todo Chatbot - Hackathon Demo",
        "version": "3.0.0-demo",
        "status": "running",
        "mode": "demo (in-memory storage)",
        "docs": "/docs",
        "note": "Simplified version for Python 3.14. Full version requires Python 3.11."
    }

@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "mode": "demo",
        "ai_provider": "Rule-based (demo)",
        "note": "Full version uses Anthropic Claude with MCP tools",
        "tools_available": ["add_task", "get_tasks", "update_task_status", "delete_task", "get_task_statistics"]
    }

@app.post("/api/{user_id}/chat", response_model=ChatResponse)
def chat(user_id: str, request: ChatRequest):
    global conversation_id_counter

    conv_id = request.conversation_id or conversation_id_counter
    if not request.conversation_id:
        conversation_id_counter += 1

    response_text, tools_used = process_message(user_id, request.message)

    return ChatResponse(
        conversation_id=conv_id,
        response=response_text,
        created_at=datetime.utcnow(),
        tools_used=tools_used if tools_used else None
    )

@app.get("/api/stats")
def global_stats():
    total_users = len(tasks_db)
    total_tasks = sum(len(tasks) for tasks in tasks_db.values())
    return {
        "total_users": total_users,
        "total_tasks": total_tasks,
        "note": "Demo mode - data resets on restart"
    }

# Mock Auth Endpoints (for demo only - Better Auth format)
@app.post("/api/auth/sign-up/email", response_model=AuthResponse)
def signup_email(request: SignupRequest):
    """Mock signup endpoint - Better Auth format - always succeeds in demo mode."""
    return AuthResponse(
        user={
            "id": "demo-user-id",
            "email": request.email,
            "name": request.name,
            "createdAt": datetime.utcnow().isoformat()
        },
        session={
            "token": "demo-token-123",
            "expiresAt": datetime.utcnow().isoformat()
        }
    )

@app.post("/api/auth/sign-in/email", response_model=AuthResponse)
def signin_email(request: LoginRequest):
    """Mock signin endpoint - Better Auth format - always succeeds in demo mode."""
    return AuthResponse(
        user={
            "id": "demo-user-id",
            "email": request.email,
            "name": "Demo User",
            "createdAt": datetime.utcnow().isoformat()
        },
        session={
            "token": "demo-token-123",
            "expiresAt": datetime.utcnow().isoformat()
        }
    )

@app.get("/api/auth/session")
def get_session():
    """Mock session endpoint."""
    return {
        "user": {
            "id": "demo-user-id",
            "email": "demo@example.com",
            "name": "Demo User"
        }
    }

if __name__ == "__main__":
    print("="*70)
    print("  AI-POWERED TODO CHATBOT - HACKATHON DEMO")
    print("="*70)
    print("  Server: http://127.0.0.1:8002")
    print("  API Docs: http://127.0.0.1:8002/docs")
    print("  Health: http://127.0.0.1:8002/api/health")
    print()
    print("  Test command:")
    print('  curl -X POST http://127.0.0.1:8002/api/demo/chat')
    print('    -H "Content-Type: application/json"')
    print('    -d \'{"message": "Add a task to buy groceries"}\'')
    print("="*70)
    uvicorn.run(app, host="127.0.0.1", port=8002)
