# Quickstart Guide: AI-Powered Todo Chatbot (Phase III)

**Feature**: 003-ai-chatbot
**Date**: 2025-12-31

## Prerequisites

Before starting, ensure you have:
- ✅ Phase II completed (full-stack web app with authentication)
- ✅ Python 3.11+ installed
- ✅ Node.js 20+ and npm installed
- ✅ PostgreSQL database (Neon) accessible
- ✅ OpenAI API key (sign up at https://platform.openai.com)
- ✅ Git repository cloned locally

## Local Development Setup

### Step 1: Install Dependencies

**Backend**:
```bash
cd backend
pip install -r requirements.txt
```

New dependencies added for Phase III:
- `openai-agents-sdk` - OpenAI Agents framework
- `mcp-sdk` - Model Context Protocol implementation
- `tenacity` - Retry logic for API calls

**Frontend**:
```bash
cd frontend
npm install
```

New dependencies added for Phase III:
- `@openai/chatkit` - Official OpenAI chat UI components

### Step 2: Configure Environment Variables

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:
```env
# Existing from Phase II
DATABASE_URL=postgresql://username:password@host/database
BETTER_AUTH_SECRET=your_secret_here
BETTER_AUTH_URL=http://localhost:3000

# NEW for Phase III
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxx
OPENAI_MODEL=gpt-4  # or gpt-4-turbo-preview
MCP_SERVER_PORT=8001  # Optional: MCP server port

# Frontend (Next.js)
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_OPENAI_DOMAIN_KEY=  # Leave empty for localhost development
```

**Note**: For local development on localhost, `NEXT_PUBLIC_OPENAI_DOMAIN_KEY` is not required. See Production Deployment section for production setup.

### Step 3: Run Database Migrations

Apply the new database migrations for conversations and messages tables:

```bash
cd backend
alembic upgrade head
```

Expected output:
```
INFO  [alembic.runtime.migration] Running upgrade xxx -> yyy, Add conversations table
INFO  [alembic.runtime.migration] Running upgrade yyy -> zzz, Add messages table
```

Verify tables created:
```bash
psql $DATABASE_URL -c "\dt"
```

You should see:
- `conversations` table
- `messages` table
- `tasks` table (existing from Phase II)
- `users` table (existing from Phase II)

### Step 4: Start Backend Server

```bash
cd backend
uvicorn main:app --reload --port 8000
```

Expected output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Registered 5 MCP tools  # <-- Confirmation of MCP tools
INFO:     Application startup complete.
```

### Step 5: Start Frontend Server

In a new terminal:
```bash
cd frontend
npm run dev
```

Expected output:
```
▲ Next.js 16.x.x
- Local:        http://localhost:3000
- Ready in 1.5s
```

### Step 6: Test the Application

1. Open browser: http://localhost:3000
2. Log in with existing Phase II credentials (or create new account)
3. Navigate to http://localhost:3000/chat
4. Send a test message: **"Add a task to buy groceries"**

Expected AI response:
```
✅ Added task: Buy groceries
```

5. Verify task created by sending: **"What's on my list?"**

Expected AI response:
```
You have 1 pending task:
1. Buy groceries
```

6. Test task completion: **"Mark buy groceries as done"**

Expected AI response:
```
✅ Marked 'Buy groceries' as complete
```

---

## Verification Checklist

After setup, verify the following:

**Backend**:
- [ ] FastAPI server running on port 8000
- [ ] MCP tools registered (check logs: "Registered 5 MCP tools")
- [ ] Database migrations applied (conversations + messages tables exist)
- [ ] Health check endpoint responding: `curl http://localhost:8000/health`

**Frontend**:
- [ ] Next.js server running on port 3000
- [ ] Chat page accessible at /chat
- [ ] ChatKit UI renders without errors
- [ ] Authentication working (JWT token passed to backend)

**Integration**:
- [ ] Chat endpoint responding: `POST http://localhost:8000/api/{user_id}/chat`
- [ ] Conversation created in database
- [ ] Messages saved to database (user + assistant)
- [ ] Tasks created via MCP tools visible in Phase II task list

**Stateless Architecture**:
- [ ] Restart backend server mid-conversation
- [ ] Refresh frontend page
- [ ] Verify conversation history persists
- [ ] Continue conversation where you left off

---

## Troubleshooting

### Issue: MCP tools not registered

**Symptom**: Logs don't show "Registered 5 MCP tools"

**Solution**:
1. Check `backend/mcp_tools/__init__.py` exists
2. Verify MCP SDK installed: `pip list | grep mcp`
3. Check for import errors in logs

### Issue: OpenAI API key not found

**Symptom**: `Error: OpenAI API key not configured`

**Solution**:
1. Ensure `.env` file exists in backend directory
2. Verify `OPENAI_API_KEY` is set and not empty
3. Restart backend server after updating `.env`

### Issue: Chat page not loading

**Symptom**: 404 error when navigating to /chat

**Solution**:
1. Verify `frontend/src/app/chat/page.tsx` exists
2. Clear Next.js cache: `rm -rf frontend/.next`
3. Restart frontend server

### Issue: Conversation history not loading

**Symptom**: Chat starts fresh every time

**Solution**:
1. Check database connection: `psql $DATABASE_URL`
2. Verify messages table has data: `SELECT * FROM messages LIMIT 10;`
3. Check browser console for errors
4. Ensure conversation_id passed in subsequent requests

### Issue: CORS errors

**Symptom**: Frontend can't connect to backend

**Solution**:
1. Verify backend CORS configuration in `main.py`
2. Check frontend `NEXT_PUBLIC_API_URL` matches backend URL
3. Ensure backend running on correct port (8000)

---

## Production Deployment

### Frontend Deployment (Vercel)

1. Deploy frontend to Vercel:
```bash
cd frontend
vercel --prod
```

2. Get production URL: `https://your-app.vercel.app`

3. Add domain to OpenAI allowlist:
   - Go to https://platform.openai.com/settings/organization/security/domain-allowlist
   - Add `your-app.vercel.app`
   - Generate domain key

4. Set environment variable in Vercel:
```bash
vercel env add NEXT_PUBLIC_OPENAI_DOMAIN_KEY production
# Paste domain key when prompted
```

5. Redeploy: `vercel --prod`

### Backend Deployment (Render/Railway)

1. Deploy backend to cloud provider (Render example):
```bash
# Create render.yaml in repository root
services:
  - type: web
    name: hackathon-todo-backend
    runtime: python
    buildCommand: pip install -r backend/requirements.txt
    startCommand: cd backend && alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: DATABASE_URL
        fromDatabase: hackathon-todo-db
      - key: OPENAI_API_KEY
        sync: false  # Set manually via dashboard
```

2. Set environment variables in Render dashboard:
   - `DATABASE_URL` - PostgreSQL connection string
   - `OPENAI_API_KEY` - Your OpenAI API key
   - `BETTER_AUTH_SECRET` - Auth secret from Phase II
   - `BETTER_AUTH_URL` - Frontend production URL

3. Deploy: `git push origin main` (triggers deploy)

4. Run migrations manually (first deploy):
```bash
render run alembic upgrade head
```

### Database (Neon - existing from Phase II)

No changes needed - Phase III migrations extend existing database.

Verify migrations applied:
```bash
psql $DATABASE_URL -c "SELECT version_num FROM alembic_version;"
```

Should show latest migration version.

---

## Docker Deployment

### Using Docker Compose

1. Build images:
```bash
docker-compose build
```

2. Start services:
```bash
docker-compose up -d
```

3. Verify services running:
```bash
docker-compose ps
```

Expected output:
```
NAME                    STATUS    PORTS
hackathon-todo-backend  Up        0.0.0.0:8000->8000/tcp
hackathon-todo-frontend Up        0.0.0.0:3000->3000/tcp
hackathon-todo-db       Up        5432/tcp
```

4. Run migrations:
```bash
docker-compose exec backend alembic upgrade head
```

5. Access application: http://localhost:3000

---

## Health Checks

### Backend Health Check

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "ok",
  "database": "connected",
  "mcp_tools": 5,
  "openai_api": "configured"
}
```

### Frontend Health Check

```bash
curl http://localhost:3000/api/health
```

Expected response:
```json
{
  "status": "ok",
  "backend": "connected"
}
```

---

## Testing

### Run Backend Tests

```bash
cd backend
pytest tests/ -v
```

Expected output:
```
tests/test_mcp_tools.py::test_add_task PASSED
tests/test_mcp_tools.py::test_get_tasks PASSED
tests/test_mcp_tools.py::test_update_task_status PASSED
tests/test_mcp_tools.py::test_delete_task PASSED
tests/test_mcp_tools.py::test_get_task_statistics PASSED
tests/test_chat_endpoint.py::test_chat_endpoint PASSED
tests/test_agent_service.py::test_agent_initialization PASSED
...
```

### Run Frontend Tests

```bash
cd frontend
npm test
```

Expected output:
```
PASS src/__tests__/chat.test.tsx
  ChatInterface
    ✓ renders without crashing
    ✓ sends message on submit
    ✓ displays conversation history
...
```

---

## Next Steps

After successful setup:

1. **Explore User Stories**: Test all 5 user stories from spec.md
2. **Monitor Logs**: Watch backend logs for tool invocations
3. **Database Inspection**: Query conversations and messages tables to see persistence
4. **Stateless Validation**: Restart backend mid-conversation and verify state recovery
5. **Performance Testing**: Test with 100+ concurrent chat requests

For implementation details, see:
- **Specification**: `specs/003-ai-chatbot/spec.md`
- **Implementation Plan**: `specs/003-ai-chatbot/plan.md`
- **Data Model**: `specs/003-ai-chatbot/data-model.md`
- **API Contracts**: `specs/003-ai-chatbot/contracts/`

---

**Need Help?**
- Check troubleshooting section above
- Review logs: `docker-compose logs backend` or `docker-compose logs frontend`
- Verify environment variables: `docker-compose config`
- Consult Phase III specifications in `specs/003-ai-chatbot/`
