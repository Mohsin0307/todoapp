# Backend Service - AI-Powered Todo App

**Phase III**: AI-Powered Chatbot with Claude (Anthropic)
**Tech Stack**: FastAPI, SQLModel, PostgreSQL, Anthropic Claude API, MCP Tools

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+ (Python 3.14 has SQLAlchemy compatibility issues)
- PostgreSQL database (Neon Serverless recommended)
- Anthropic API key

### Installation

```bash
# Create virtual environment
python3.11 -m venv .venv

# Activate virtual environment
source .venv/Scripts/activate  # Windows Git Bash
source .venv/bin/activate      # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head
```

### Configuration

Create `.env` file from `.env.example`:

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```bash
# Database
DATABASE_URL=postgresql+asyncpg://user:password@host/database

# Authentication
JWT_SECRET=your-secret-key-min-32-characters

# Claude AI (Phase III)
ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
ANTHROPIC_MAX_TOKENS=2048

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://frontend:3000
```

### Run Server

```bash
# Development mode (with auto-reload)
uvicorn main:app --reload --port 8000

# OR use the standalone chat server (bypasses database)
uvicorn chat_with_tools:app --reload --port 8001

# Production mode
uvicorn main:app --host 0.0.0.0 --port 8000
```

---

## 📁 Project Structure

```
backend/
├── main.py                    # Main FastAPI application
├── chat_standalone.py         # Standalone chat (no database)
├── chat_with_tools.py         # Tool-enabled chat server
├── requirements.txt           # Python dependencies
├── alembic/                   # Database migrations
│   ├── env.py
│   └── versions/
├── src/
│   ├── api/                   # API routes
│   │   ├── auth.py           # Authentication endpoints
│   │   ├── tasks.py          # Task CRUD endpoints
│   │   ├── chat.py           # Chat endpoint (Phase III)
│   │   └── health.py         # Health check endpoint
│   ├── models/               # SQLModel database models
│   │   ├── user.py
│   │   ├── task.py
│   │   ├── conversation.py   # Phase III
│   │   └── message.py        # Phase III
│   ├── services/             # Business logic
│   │   ├── agent_service.py  # Claude agent service
│   │   └── conversation_service.py
│   ├── config.py             # Configuration settings
│   └── database.py           # Database connection
└── mcp_tools/                # MCP Tools (Phase III)
    ├── __init__.py           # Tool registry
    └── task_tools.py         # 5 task management tools
```

---

## 🤖 Phase III: AI Chatbot Features

### MCP Tools API Reference

The backend implements 5 Model Context Protocol (MCP) tools for Claude:

#### 1. **add_task**
Creates a new task from natural language.

**Input Schema**:
```json
{
  "title": "string (required)",
  "description": "string (optional)"
}
```

**Example**:
```python
result = add_task_tool(
    title="Buy groceries",
    description="Milk, eggs, bread",
    user_id="user123"
)
```

**Response**:
```json
{
  "success": true,
  "task_id": 42,
  "title": "Buy groceries",
  "message": "✅ Created task: Buy groceries"
}
```

#### 2. **get_tasks**
Retrieves tasks with optional status filtering.

**Input Schema**:
```json
{
  "status": "pending | completed (optional)"
}
```

**Example**:
```python
result = get_tasks_tool(status="pending", user_id="user123")
```

**Response**:
```json
{
  "success": true,
  "tasks": [
    {
      "id": 1,
      "title": "Buy groceries",
      "status": "pending",
      "created_at": "2025-12-31T10:00:00"
    }
  ],
  "count": 1,
  "filter": "pending"
}
```

#### 3. **update_task_status**
Updates task completion status.

**Input Schema**:
```json
{
  "task_id": "integer (required)",
  "status": "completed | pending (required)"
}
```

**Example**:
```python
result = update_task_status_tool(
    task_id=42,
    status="completed",
    user_id="user123"
)
```

#### 4. **delete_task**
Permanently deletes a task.

**Input Schema**:
```json
{
  "task_id": "integer (required)"
}
```

#### 5. **get_task_statistics**
Returns productivity insights.

**Response**:
```json
{
  "success": true,
  "statistics": {
    "total_tasks": 10,
    "pending_tasks": 7,
    "completed_tasks": 3,
    "completion_rate": 30.0,
    "tasks_created_today": 2,
    "tasks_completed_today": 1,
    "streak_days": 5
  }
}
```

### Chat Endpoint Documentation

#### POST `/api/{user_id}/chat`

Process chat message and return Claude AI response with tool execution.

**Request**:
```json
{
  "message": "Show my pending tasks",
  "conversation_id": 123  // Optional, null for new conversation
}
```

**Response**:
```json
{
  "conversation_id": 123,
  "response": "You have 3 pending tasks:\n1. Buy groceries\n2. Call dentist\n3. Finish report",
  "created_at": "2025-12-31T12:00:00Z",
  "tools_used": ["get_tasks"]  // Tools invoked during response
}
```

**Authentication**: Requires JWT token in Authorization header
```
Authorization: Bearer <your-jwt-token>
```

**Flow**:
1. User sends natural language message
2. Backend loads conversation history (last 50 messages)
3. Claude agent processes message with available tools
4. Tools execute (e.g., fetch tasks from database)
5. Claude generates natural language response
6. Both user message and assistant response saved to database

### Agent Configuration Guide

The Claude agent is configured in `chat_with_tools.py`:

```python
# System prompt defines agent behavior
system_prompt = """You are a helpful AI assistant for task management.
You help users:
- Create new tasks from natural language
- View and filter their task lists
- Update task status (complete/pending)
- Delete tasks
- Get productivity insights

Be concise, friendly, and use emojis appropriately."""

# Agent configuration
client = Anthropic(api_key=api_key)
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=2048,
    system=system_prompt,
    tools=mcp_tools,  # 5 tools available
    messages=conversation_history
)
```

**Key Configuration Parameters**:
- `model`: Claude model version (sonnet, opus, haiku)
- `max_tokens`: Maximum response length (2048 recommended)
- `system`: System prompt defining agent behavior
- `tools`: List of MCP tools available to agent
- `messages`: Conversation history for context

**Conversation Windowing**:
- Last 50 messages loaded from database
- Reduces token usage while maintaining context
- Configurable in `conversation_service.py`

---

## 🔧 Environment Variables

### Required

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql+asyncpg://user:pass@host/db` |
| `JWT_SECRET` | Secret key for JWT tokens (min 32 chars) | `your-super-secret-key-here` |
| `ANTHROPIC_API_KEY` | Anthropic API key for Claude | `sk-ant-api03-xxx` |

### Optional

| Variable | Description | Default |
|----------|-------------|---------|
| `ANTHROPIC_MODEL` | Claude model to use | `claude-3-5-sonnet-20241022` |
| `ANTHROPIC_MAX_TOKENS` | Max tokens in response | `2048` |
| `ALLOWED_ORIGINS` | CORS allowed origins (comma-separated) | `http://localhost:3000` |
| `JWT_ALGORITHM` | JWT signing algorithm | `HS256` |
| `JWT_EXPIRATION_HOURS` | JWT token lifetime | `24` |
| `HOST` | Server bind address | `0.0.0.0` |
| `PORT` | Server port | `8000` |
| `LOG_LEVEL` | Logging level | `info` |

---

## 🩺 Health Check

### GET `/api/health`

Returns system health status including database and MCP tools.

**Response**:
```json
{
  "status": "ok",
  "ai_provider": "Anthropic Claude",
  "model": "claude-3-5-sonnet-20241022",
  "api_configured": true,
  "tools_registered": 5,
  "tool_names": [
    "add_task",
    "get_tasks",
    "update_task_status",
    "delete_task",
    "get_task_statistics"
  ],
  "message": "Chat endpoint with tool use ready"
}
```

---

## 🐛 Troubleshooting

### Python 3.14 Compatibility Issue

**Symptom**: SQLAlchemy fails with `AssertionError` during imports

**Cause**: Python 3.14 is too new for current SQLAlchemy version

**Solution**:
```bash
# Downgrade to Python 3.11
python3.11 -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
```

### Anthropic Client Error: "unexpected keyword argument 'proxies'"

**Symptom**: Chat endpoint returns client initialization error

**Cause**: httpx version conflict or environment proxy settings

**Solutions**:
```bash
# Update httpx
pip install --upgrade httpx anthropic

# Check for proxy environment variables
env | grep -i proxy

# If found, unset them
unset HTTP_PROXY HTTPS_PROXY
```

### Database Connection Errors

**Symptom**: `FATAL: password authentication failed`

**Solutions**:
1. Verify `DATABASE_URL` in `.env`
2. Check PostgreSQL is running
3. Test connection manually:
```bash
psql "postgresql://user:pass@host/db"
```

### Port Already in Use

**Symptom**: `Address already in use`

**Solutions**:
```bash
# Find process on port 8000
netstat -ano | findstr :8000  # Windows
lsof -i :8000                 # Linux/Mac

# Kill the process
taskkill /PID <PID> /F        # Windows
kill -9 <PID>                 # Linux/Mac

# OR use different port
uvicorn main:app --port 8001
```

### Migration Errors

**Symptom**: `Can't locate revision`

**Solutions**:
```bash
# Reset migrations (⚠️ destroys data)
alembic downgrade base
alembic upgrade head

# OR generate new migration
alembic revision --autogenerate -m "description"
alembic upgrade head
```

### Tool Not Found Errors

**Symptom**: MCP tool execution fails

**Cause**: Tools not registered at startup

**Solution**:
```python
# Verify tools are imported in chat_with_tools.py
from mcp_tools.task_tools import get_all_tools

# Check health endpoint shows 5 tools
curl http://localhost:8001/api/health
```

---

## 📝 API Documentation

Full API documentation available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_chat.py

# Run with verbose output
pytest -v -s
```

---

## 📦 Dependencies

Key dependencies (see `requirements.txt` for full list):

- **FastAPI** (0.115.0): Web framework
- **SQLModel** (0.0.22): ORM for database
- **Anthropic** (0.39.0): Claude AI SDK
- **Alembic** (1.13.3): Database migrations
- **python-jose** (3.3.0): JWT authentication
- **asyncpg** (0.29.0): PostgreSQL async driver

---

## 🚢 Deployment

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop services
docker-compose down
```

### Manual Deployment

1. Set up Python 3.11 environment
2. Install dependencies
3. Configure environment variables
4. Run migrations
5. Start with production server:

```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

---

## 📚 Additional Resources

- **Anthropic Documentation**: https://docs.anthropic.com/
- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **SQLModel Documentation**: https://sqlmodel.tiangolo.com/
- **Alembic Documentation**: https://alembic.sqlalchemy.org/

---

**For frontend integration, see**: `../frontend/README.md`
**For full project setup, see**: `../README.md`
