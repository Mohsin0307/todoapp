# Quick Start Guide - Phase III AI Chatbot with Claude

## 🚀 Getting Started (5 Minutes)

### Step 1: Install Dependencies

Open Git Bash in the backend directory:

```bash
cd ~/Desktop/hackton2/mytodoap/backend

# Activate your venv
source venv/Scripts/activate

# Install all dependencies (including Anthropic SDK)
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed anthropic-0.39.0 ...
```

### Step 2: Configure Claude API Key

1. Get your Anthropic API key from: https://console.anthropic.com/settings/keys

2. Create/edit `backend/.env`:

```bash
cd ~/Desktop/hackton2/mytodoap/backend
cp .env.example .env
nano .env  # or use your preferred editor
```

3. Add your API key to `.env`:

```bash
# Find and update these lines:
ANTHROPIC_API_KEY=sk-ant-api03-YOUR-ACTUAL-KEY-HERE
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
ANTHROPIC_MAX_TOKENS=2048
```

4. **Save the file** (Ctrl+O, Enter, Ctrl+X if using nano)

### Step 3: Start the Backend Server

```bash
cd ~/Desktop/hackton2/mytodoap/backend

# Activate venv (if not already active)
source venv/Scripts/activate

# Start server using python -m
python -m uvicorn main:app --reload --port 8000
```

**Expected output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**✅ Backend is running!** Leave this terminal open.

### Step 4: Start the Frontend

Open a **NEW** Git Bash terminal:

```bash
cd ~/Desktop/hackton2/mytodoap/frontend

# Install dependencies (if not already done)
npm install

# Start development server
npm run dev
```

**Expected output:**
```
▲ Next.js 15.x
- Local:        http://localhost:3000
- Ready in 2.3s
```

**✅ Frontend is running!**

### Step 5: Test the Chatbot!

1. Open your browser: **http://localhost:3000/chat**

2. Try these messages:
   - "help" - Get setup instructions
   - "add a task to buy groceries" - Create a task
   - "show my tasks" - View tasks
   - "hello" - Chat with Claude!

---

## 🔧 Troubleshooting

### Problem: "uvicorn: command not found"

**Solution:**
```bash
cd ~/Desktop/hackton2/mytodoap/backend
source venv/Scripts/activate
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000
```

**Why this works:** Using `python -m uvicorn` instead of just `uvicorn` ensures Python finds the module.

### Problem: "ModuleNotFoundError: No module named 'anthropic'"

**Solution:**
```bash
cd ~/Desktop/hackton2/mytodoap/backend
source venv/Scripts/activate
pip install anthropic==0.39.0
```

### Problem: Backend shows SQLAlchemy error

**Solution:** This is a known Python 3.14 compatibility issue. The chat endpoint will still work for basic responses! To fully fix:

**Option 1 - Use Python 3.11 (Recommended):**
```bash
# Install Python 3.11 from python.org
# Then recreate venv:
cd ~/Desktop/hackton2/mytodoap/backend
rm -rf venv
python3.11 -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
```

**Option 2 - Use Docker:**
```bash
cd ~/Desktop/hackton2/mytodoap
docker-compose up
```

### Problem: "Port 8000 already in use"

**Solution:** Use a different port:
```bash
python -m uvicorn main:app --reload --port 8001
```

Then update frontend fetch URL in `frontend/app/chat/page.tsx` line 51:
```typescript
const response = await fetch("http://localhost:8001/api/demo-user/chat", {
```

### Problem: Chat endpoint returns "API not configured"

**Solution:** Make sure you:
1. Added your actual Anthropic API key to `backend/.env`
2. Restarted the backend server after adding the key
3. Your API key starts with `sk-ant-api03-`

Check configuration:
```bash
curl http://localhost:8000/api/health
```

Should return:
```json
{
  "status": "ok",
  "ai_provider": "Anthropic Claude",
  "model": "claude-3-5-sonnet-20241022",
  "api_configured": true,
  "message": "Chat endpoint ready"
}
```

---

## 📝 What's Working

### ✅ Currently Functional

1. **Backend Server** - FastAPI running on port 8000
2. **Chat Endpoint** - POST `/api/{user_id}/chat`
3. **Claude Integration** - Real AI responses when API key is configured
4. **Frontend Chat UI** - React chat interface at `/chat`
5. **Placeholder Responses** - Helpful messages when API key is not set

### 🚧 In Progress

1. **Database Integration** - Blocked by Python 3.14/SQLAlchemy issue
2. **MCP Tools** - Task operations (add, list, update, delete)
3. **Conversation History** - Persistent chat sessions
4. **Full Authentication** - JWT integration with chat

### 🎯 Next Steps (After Setup)

Once you have the servers running and Claude configured:

1. **Test Claude Responses:**
   - Try different task management queries
   - See how Claude responds naturally

2. **Fix Python Environment** (Optional but recommended):
   - Downgrade to Python 3.11 for full database support
   - OR use Docker: `docker-compose up`

3. **Implement MCP Tools:**
   - Add actual task operations
   - Connect to database
   - Enable persistent conversations

4. **Complete User Stories:**
   - Natural language task creation
   - Conversational task retrieval
   - Status updates and analytics

---

## 🎓 Key Changes Made

### From OpenAI to Claude

1. **Dependencies:**
   - ❌ Removed: `openai==1.55.0`
   - ✅ Added: `anthropic==0.39.0`

2. **Environment Variables:**
   - ❌ `OPENAI_API_KEY`
   - ✅ `ANTHROPIC_API_KEY`
   - ✅ `ANTHROPIC_MODEL`
   - ✅ `ANTHROPIC_MAX_TOKENS`

3. **API Integration:**
   - Using Anthropic SDK instead of OpenAI SDK
   - Claude 3.5 Sonnet model (best for chat)
   - Async message creation
   - System prompts for task management

### Why Claude?

- **Latest Model**: Claude 3.5 Sonnet (October 2024)
- **Better Context**: 200K token context window
- **Cost Effective**: Competitive pricing
- **User Request**: You asked for Claude instead of OpenAI!

---

## 📚 Helpful Commands

### Backend

```bash
# Activate venv
cd ~/Desktop/hackton2/mytodoap/backend
source venv/Scripts/activate

# Install dependencies
pip install -r requirements.txt

# Run server
python -m uvicorn main:app --reload --port 8000

# Test health endpoint
curl http://localhost:8000/api/health

# Test chat endpoint
curl -X POST http://localhost:8000/api/demo-user/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "hello", "conversation_id": null}'
```

### Frontend

```bash
# Install dependencies
cd ~/Desktop/hackton2/mytodoap/frontend
npm install

# Run development server
npm run dev

# Build for production
npm run build
npm start
```

---

## 🎉 Success Checklist

- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] Can access http://localhost:3000/chat
- [ ] Chat UI loads without errors
- [ ] Can send messages in chat
- [ ] Receiving Claude AI responses (if API key configured)
- [ ] OR receiving helpful placeholder responses (if API key not yet configured)

**All set? Start chatting with your AI-powered todo assistant!** 🚀

---

Need help? Check:
- Backend logs in the terminal where uvicorn is running
- Browser console (F12) for frontend errors
- `IMPLEMENTATION_STATUS.md` for detailed project status
