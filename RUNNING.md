# Running the Application - Phase III AI Chatbot

## Current Status: Chat-Only Mode ✅

The application is currently running in **chat-only mode** to bypass Python 3.14/SQLAlchemy compatibility issues. This allows you to test the Claude AI chatbot integration while database features are being resolved.

## ✅ What's Currently Running

### Backend (Port 8001)
- **Status**: ✅ Running (`chat_standalone.py`)
- **URL**: http://localhost:8001
- **Features**:
  - Chat endpoint: `POST /api/{user_id}/chat`
  - Health check: `GET /api/health`
  - Placeholder AI responses (Claude API key not configured)
- **Note**: Database features temporarily disabled

### Frontend (Port 3000)
- **Status**: ✅ Running (Next.js dev server)
- **URL**: http://localhost:3000
- **Chat UI**: http://localhost:3000/chat
- **Features**:
  - Custom chat interface
  - Real-time messaging
  - Claude AI integration (pending API key)

## 🚀 Quick Start

### 1. Backend is Already Running!
The backend is running on port 8001 using `chat_standalone.py`. To restart:

```bash
cd backend
source .venv/Scripts/activate
python -m uvicorn chat_standalone:app --reload --port 8001
```

### 2. Frontend is Already Running!
The frontend is running on port 3000. To restart:

```bash
cd frontend
npm run dev
```

### 3. Test the Chat
Open your browser and go to: **http://localhost:3000/chat**

Try these messages:
- `help` - Get setup instructions
- `add a task to buy groceries` - See placeholder response
- `hello` - Chat with the assistant

## 🔑 Enable Claude AI (Optional)

To activate real Claude AI responses:

### 1. Get Anthropic API Key
Visit: https://console.anthropic.com/settings/keys

### 2. Create `.env` file
```bash
cd backend
cp .env.example .env
```

### 3. Edit `.env` and add your key:
```bash
ANTHROPIC_API_KEY=sk-ant-api03-YOUR-ACTUAL-KEY-HERE
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
ANTHROPIC_MAX_TOKENS=2048
```

### 4. Restart Backend
```bash
# Kill the current server (Ctrl+C)
python -m uvicorn chat_standalone:app --reload --port 8001
```

### 5. Test Claude AI
Go to http://localhost:3000/chat and ask:
- "Hello, how can you help me?"
- "Add a task to learn Python"

You'll now get real Claude AI responses! 🎉

## 📁 File Structure

```
mytodoap/
├── backend/
│   ├── chat_standalone.py      # ✅ Current server (chat-only)
│   ├── main.py                 # ❌ Blocked by Python 3.14 issue
│   ├── .env                    # Your API key goes here
│   └── .venv/                  # Python virtual environment
├── frontend/
│   ├── app/chat/page.tsx       # ✅ Chat UI (updated for port 8001)
│   └── package.json
└── RUNNING.md                  # This file
```

## ⚠️ Known Issues & Workarounds

### Python 3.14 Compatibility Issue
**Problem**: SQLAlchemy doesn't work with Python 3.14, blocking database features.

**Current Workaround**: Using `chat_standalone.py` which bypasses all database imports.

**Future Fix Options**:
1. Downgrade to Python 3.11
2. Wait for SQLAlchemy update
3. Use Docker (python:3.11-slim base image)

### Port 8000 Access Denied
**Problem**: Port 8000 is blocked on Windows.

**Workaround**: Using port 8001 instead (frontend updated).

## 🧪 Testing Endpoints

### Health Check
```bash
curl http://localhost:8001/api/health
```

Expected response:
```json
{
  "status": "ok",
  "ai_provider": "Anthropic Claude",
  "model": "claude-3-5-sonnet-20241022",
  "api_configured": false,
  "message": "Chat endpoint ready (awaiting API key configuration)"
}
```

### Chat Endpoint
```bash
curl -X POST http://localhost:8001/api/demo-user/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "help", "conversation_id": null}'
```

Expected response:
```json
{
  "conversation_id": 1,
  "response": "🤖 **Claude AI Todo Chatbot**...",
  "created_at": "2025-12-31T..."
}
```

## 📊 What Works Right Now

✅ **Working Features**:
- Backend server on port 8001
- Frontend on port 3000
- Chat UI at /chat route
- Chat endpoint with placeholder responses
- Health check endpoint
- CORS configured
- Error handling

❌ **Pending Features** (blocked by Python 3.14 issue):
- Database persistence
- User authentication integration
- Task operations (add, list, update, delete)
- Conversation history storage
- MCP tools integration
- Full Claude Agents SDK integration

## 🎯 Next Steps

### Immediate
1. ✅ Backend running on port 8001
2. ✅ Frontend running on port 3000
3. ✅ Chat UI accessible
4. ⏳ Add Anthropic API key to enable Claude AI

### Short Term (After API Key)
5. Test Claude AI responses
6. Verify natural language understanding
7. Document user interactions

### Long Term (After Python Fix)
8. Fix Python 3.14/SQLAlchemy compatibility
9. Implement database persistence
10. Add MCP tools for task operations
11. Integrate full Claude Agents SDK
12. Complete all 94 Phase III tasks

## 🆘 Troubleshooting

### Backend Won't Start
```bash
# Check if port 8001 is free
netstat -ano | findstr :8001

# Kill any process using port 8001
taskkill /PID <PID> /F

# Start backend
cd backend
source .venv/Scripts/activate
python -m uvicorn chat_standalone:app --reload --port 8001
```

### Frontend Won't Start
```bash
# Kill any Node process
taskkill /IM node.exe /F

# Reinstall dependencies
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### Chat Not Working
1. Check backend is running: http://localhost:8001/api/health
2. Check frontend is running: http://localhost:3000
3. Open browser console (F12) for errors
4. Verify fetch URL is http://localhost:8001 (not 8000)

## 📚 Documentation

- **Setup Guide**: `QUICK_START.md`
- **Implementation Status**: `IMPLEMENTATION_STATUS.md`
- **This File**: `RUNNING.md` - Current server status

---

**🎉 Your chatbot is ready to test!**

Go to http://localhost:3000/chat and start chatting!
