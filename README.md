# AI-Powered Todo Application

A multi-phase task management system evolving from console app → web app → AI chatbot.

**Current Phase**: Phase III - AI-Powered Chatbot with Claude
**Tech Stack**: Python (FastAPI), TypeScript (Next.js), PostgreSQL, Anthropic Claude AI

---

## 📚 Project Phases

### Phase I: Console Application ✅ Complete
Simple in-memory CLI todo list with CRUD operations.

**Features**:
- Add, view, update, delete tasks
- Mark tasks complete
- In-memory storage
- TDD development (108 tests)

**Status**: Foundational complete, archived in `src/` directory

---

### Phase II: Full-Stack Web Application ✅ Complete
Multi-user web app with authentication and database.

**Features**:
- User authentication (Better Auth + JWT)
- RESTful API (FastAPI)
- PostgreSQL database (Neon Serverless)
- React frontend (Next.js 16)
- Docker deployment
- Per-user task isolation

**Status**: Production-ready baseline

**Stack**:
- Backend: FastAPI + SQLModel + Alembic
- Frontend: Next.js + Better Auth + Tailwind
- Database: PostgreSQL (Neon)

---

### Phase III: AI-Powered Chatbot ⚡ In Progress
Natural language task management with Claude AI.

**Features**:
- Conversational task management
- Claude 3.5 Sonnet AI agent
- 5 MCP tools for task operations
- Tool-based function calling
- Conversation persistence
- Stateless architecture

**Status**: Core infrastructure complete (29% of tasks)
- ✅ MCP tools framework
- ✅ Chat endpoint with Claude
- ✅ Custom React chat UI
- ⚠️ Database blocked by Python 3.14 issue

**Stack**:
- AI: Anthropic Claude 3.5 Sonnet
- Tools: MCP protocol (5 task tools)
- Same backend/frontend as Phase II + chat features

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND (Next.js 16)                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  Task UI     │  │  Auth Pages  │  │  Chat UI     │          │
│  │  (Phase II)  │  │  (Phase II)  │  │  (Phase III) │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│         │                  │                  │                  │
│         └──────────────────┴──────────────────┘                  │
│                            │                                     │
│                    HTTP / REST API                               │
└─────────────────────────────────────────────────────────────────┘
                             │
┌─────────────────────────────────────────────────────────────────┐
│                      BACKEND (FastAPI)                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  Task API    │  │  Auth API    │  │  Chat API    │          │
│  │  (Phase II)  │  │  (Phase II)  │  │  (Phase III) │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│         │                  │                  │                  │
│         │                  │          ┌───────┴──────┐           │
│         │                  │          │ Claude Agent │           │
│         │                  │          │   Service    │           │
│         │                  │          └───────┬──────┘           │
│         │                  │                  │                  │
│         │                  │          ┌───────┴──────┐           │
│         │                  │          │  MCP Tools   │           │
│         │                  │          │ • add_task   │           │
│         │                  │          │ • get_tasks  │           │
│         │                  │          │ • update     │           │
│         │                  │          │ • delete     │           │
│         │                  │          │ • statistics │           │
│         │                  │          └───────┬──────┘           │
│         └──────────────────┴──────────────────┘                  │
│                            │                                     │
│                    SQLModel ORM                                  │
└─────────────────────────────────────────────────────────────────┘
                             │
┌─────────────────────────────────────────────────────────────────┐
│                    DATABASE (PostgreSQL)                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │    Users     │  │    Tasks     │  │Conversations │          │
│  │  (Phase II)  │  │  (Phase II)  │  │ (Phase III)  │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                      ┌──────────────┐            │
│                                      │   Messages   │            │
│                                      │ (Phase III)  │            │
│                                      └──────────────┘            │
└─────────────────────────────────────────────────────────────────┘
                             │
┌─────────────────────────────────────────────────────────────────┐
│                  EXTERNAL SERVICES                               │
│  ┌──────────────────────┐    ┌──────────────────────┐          │
│  │  Anthropic Claude    │    │   Neon PostgreSQL    │          │
│  │  (AI Provider)       │    │   (Database Host)    │          │
│  └──────────────────────┘    └──────────────────────┘          │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+** (NOT 3.14 - SQLAlchemy compatibility issue)
- **Node.js 20+**
- **PostgreSQL** (or Neon account)
- **Anthropic API Key** (for Phase III features)

### Setup (All Phases)

#### 1. Clone Repository

```bash
git clone <repo-url>
cd mytodoap
```

#### 2. Backend Setup

```bash
cd backend

# Create virtual environment (Python 3.11!)
python3.11 -m venv .venv

# Activate venv
source .venv/Scripts/activate  # Windows Git Bash
source .venv/bin/activate      # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your credentials:
# - DATABASE_URL (PostgreSQL connection)
# - JWT_SECRET (min 32 chars)
# - ANTHROPIC_API_KEY (for Phase III)

# Run migrations
alembic upgrade head

# Start server
uvicorn main:app --reload --port 8000
```

**Backend URL**: http://localhost:8000

#### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env.local
# Edit .env.local:
# - BETTER_AUTH_SECRET (same as backend JWT_SECRET)
# - NEXT_PUBLIC_API_URL=http://localhost:8000

# Start development server
npm run dev
```

**Frontend URL**: http://localhost:3000

#### 4. Test Phase III Chat

Open http://localhost:3000/chat and try:
- "help" - Setup instructions
- "add a task to buy groceries"
- "show my pending tasks"

---

## 🐳 Docker Setup (Recommended)

### Quick Start with Docker

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

**Services**:
- Backend: http://localhost:8000
- Frontend: http://localhost:3000
- Database: PostgreSQL on port 5432

### Docker Configuration

See `docker-compose.yml` for full configuration.

**Environment Variables** (set in docker-compose.yml):
- `DATABASE_URL`
- `JWT_SECRET`
- `ANTHROPIC_API_KEY`
- `ANTHROPIC_MODEL`

---

## 📖 Manual Setup (Without Docker)

### Step 1: Database Setup

**Option A: Neon (Recommended)**
1. Create account at https://neon.tech
2. Create database
3. Copy connection string to `backend/.env`

**Option B: Local PostgreSQL**
```bash
# Install PostgreSQL
# Create database
createdb todo_app

# Connection string format:
# DATABASE_URL=postgresql+asyncpg://user:password@localhost/todo_app
```

### Step 2: Backend

```bash
cd backend
source .venv/Scripts/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn main:app --reload --port 8000
```

**Verify**: http://localhost:8000/api/health

### Step 3: Frontend

```bash
cd frontend
npm install
npm run dev
```

**Verify**: http://localhost:3000

### Step 4: Create User Account

1. Navigate to http://localhost:3000
2. Click "Sign Up"
3. Create account
4. Login

### Step 5: Test Phase III Chat

1. Navigate to http://localhost:3000/chat
2. Send message: "add a task to learn Claude"
3. Verify AI response

---

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest tests/ -v

# With coverage
pytest --cov=src --cov-report=html tests/
```

### Frontend Tests

```bash
cd frontend
npm test

# E2E tests
npm run test:e2e
```

---

## 📝 API Documentation

### Interactive Docs

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

#### Phase II (Tasks)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Create account |
| POST | `/api/auth/login` | Get JWT token |
| GET | `/api/{user_id}/tasks` | List user's tasks |
| POST | `/api/{user_id}/tasks` | Create task |
| PUT | `/api/{user_id}/tasks/{id}` | Update task |
| DELETE | `/api/{user_id}/tasks/{id}` | Delete task |

#### Phase III (Chat)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/{user_id}/chat` | Send chat message |
| GET | `/api/health` | Health check + tool status |
| GET | `/api/tools` | List available MCP tools |

---

## 🛠️ Development Guide

### Project Structure

```
mytodoap/
├── backend/              # FastAPI backend
│   ├── src/
│   │   ├── api/         # Route handlers
│   │   ├── models/      # Database models
│   │   └── services/    # Business logic
│   ├── mcp_tools/       # Phase III tools
│   ├── alembic/         # Migrations
│   └── main.py          # App entry
├── frontend/            # Next.js frontend
│   ├── app/
│   │   ├── tasks/       # Task management UI
│   │   └── chat/        # Phase III chat UI
│   ├── components/      # Reusable components
│   └── lib/             # Utilities
├── specs/               # Feature specifications
│   ├── 001-console-app/
│   ├── 002-fullstack-web/
│   └── 003-ai-chatbot/
├── docker-compose.yml   # Docker orchestration
└── README.md           # This file
```

### Adding New Features

1. **Write Specification**: Create spec in `specs/00X-feature-name/`
2. **Generate Tasks**: Run `/sp.tasks` to create task breakdown
3. **Implement**: Follow TDD approach
4. **Test**: Write tests for all functionality
5. **Document**: Update relevant README files

### Database Migrations

```bash
# Create migration
cd backend
alembic revision --autogenerate -m "description"

# Apply migration
alembic upgrade head

# Rollback
alembic downgrade -1
```

---

## 🐛 Troubleshooting

### Common Issues

#### 1. Python 3.14 Compatibility Error

**Symptom**: `AssertionError` in SQLAlchemy

**Solution**:
```bash
# Use Python 3.11
python3.11 -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
```

#### 2. Database Connection Failed

**Symptom**: `could not connect to server`

**Solutions**:
- Verify `DATABASE_URL` in `.env`
- Check PostgreSQL is running
- Test connection: `psql "your-database-url"`

#### 3. Frontend Can't Connect to Backend

**Symptom**: Network error in browser console

**Solutions**:
- Verify backend is running: http://localhost:8000/api/health
- Check CORS settings in `backend/main.py`
- Verify `NEXT_PUBLIC_API_URL` in `frontend/.env.local`

#### 4. Claude API Not Working

**Symptom**: Chat returns error messages

**Solutions**:
- Verify `ANTHROPIC_API_KEY` is set in `backend/.env`
- Check API key is valid at https://console.anthropic.com
- Test with standalone server: `uvicorn chat_with_tools:app --port 8001`

#### 5. Port Already in Use

**Symptom**: `Address already in use`

**Solutions**:
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :8000
kill -9 <PID>
```

### Getting Help

1. Check `backend/README.md` for backend-specific issues
2. Check `frontend/README.md` for frontend-specific issues
3. Review `PHASE3_IMPLEMENTATION_SUMMARY.md` for current status
4. Check `RUNNING.md` for server management guide

---

## 📊 Current Status

**Phase I**: ✅ 100% Complete (Console app archived)
**Phase II**: ✅ 100% Complete (Full-stack web app)
**Phase III**: ⚡ 29% Complete (AI chatbot)

**Phase III Progress**:
- ✅ Setup (5/5 tasks)
- ⚡ Foundational (17/31 tasks) - 55%
  - ✅ Database models created
  - ✅ MCP tools framework complete
  - ⚡ Chat endpoint partial
  - ❌ Database integration blocked
- ⚡ User Stories (0/35 tasks)
- ⚡ Frontend (2/12 tasks)
- ✅ Documentation (6/11 tasks)

**Blockers**:
- Python 3.14/SQLAlchemy compatibility
- Anthropic client httpx issue

**Next Steps**:
1. Fix Python environment → Python 3.11
2. Complete database integration
3. Implement remaining user stories
4. Polish frontend components

---

## 🚢 Deployment

### Production Checklist

- [ ] Set strong `JWT_SECRET` (min 32 chars)
- [ ] Configure production `DATABASE_URL`
- [ ] Add valid `ANTHROPIC_API_KEY`
- [ ] Set `NODE_ENV=production`
- [ ] Build frontend: `npm run build`
- [ ] Run migrations: `alembic upgrade head`
- [ ] Set up SSL/TLS certificates
- [ ] Configure reverse proxy (nginx)
- [ ] Set up monitoring (e.g., Sentry)
- [ ] Configure backups for database

### Deployment Options

**Option 1: Docker**
```bash
docker-compose -f docker-compose.prod.yml up -d
```

**Option 2: Vercel (Frontend) + Railway (Backend)**
- Deploy frontend to Vercel
- Deploy backend to Railway
- Configure environment variables

**Option 3: Manual VPS**
- Set up nginx as reverse proxy
- Use systemd for process management
- Configure PostgreSQL backups

---

## 📚 Documentation

- **Backend API**: `backend/README.md`
- **Frontend Guide**: `frontend/README.md`
- **Running Servers**: `RUNNING.md`
- **Implementation Status**: `PHASE3_IMPLEMENTATION_SUMMARY.md`
- **Quick Start**: `QUICK_START.md`

## 🤝 Contributing

This is a learning project demonstrating:
- Spec-driven development
- Multi-phase feature evolution
- Modern full-stack architecture
- AI integration patterns

Feel free to fork and modify for your own use.

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🎯 Learning Outcomes

This project demonstrates:

1. **Phase Evolution**: Console → Web → AI
2. **Modern Stack**: FastAPI + Next.js + PostgreSQL + Claude
3. **Authentication**: JWT + Better Auth
4. **AI Integration**: Claude 3.5 Sonnet + MCP tools
5. **Database**: SQLModel + Alembic migrations
6. **Docker**: Multi-service orchestration
7. **TDD**: Test-driven development
8. **Spec-Driven**: Feature specifications → Implementation

---

**Ready to start?** See [Quick Start](#-quick-start) above!

**Questions?** Check [Troubleshooting](#-troubleshooting) or the README files in `backend/` and `frontend/` directories.
# todoapp
