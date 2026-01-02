# Quickstart: Phase II Full-Stack Web Application

**Last Updated**: 2025-12-30
**Purpose**: Complete setup guide for local development of the Phase II todo application

---

## Prerequisites

Before starting, ensure you have the following installed:

- **Docker** 24+ and **Docker Compose** 2+ ([Install Docker Desktop](https://docs.docker.com/get-docker/))
- **Node.js** 18+ and **npm** 9+ (for local frontend development) - [Install Node.js](https://nodejs.org/)
- **Python** 3.11+ and **pip** (for local backend development) - [Install Python](https://www.python.org/downloads/)
- **Git** 2.40+ for version control
- **Neon Account** with PostgreSQL database created - [Sign up](https://neon.tech/)

**Optional**:
- **Visual Studio Code** with Docker extension
- **Postman** or **Thunder Client** for API testing

---

## Quick Start (Docker Compose)

**Fastest way to get the entire stack running:**

```bash
# 1. Clone repository
git clone <repo-url>
cd mytodoap

# 2. Checkout Phase II branch
git checkout 002-phase2-fullstack-setup

# 3. Copy environment templates
cp backend/.env.example backend/.env
cp frontend/.env.local.example frontend/.env.local

# 4. Edit .env files with your values (see Environment Setup below)

# 5. Start all services
docker-compose up --build

# 6. Run database migrations (in new terminal)
docker-compose exec backend alembic upgrade head

# 7. Access the application
#    - Frontend: http://localhost:3000
#    - Backend API: http://localhost:8000
#    - API Docs: http://localhost:8000/docs
```

**That's it!** The application is running. Continue to Environment Setup for details.

---

## Environment Setup

### Step 1: Create Neon Database

1. Go to [Neon Dashboard](https://console.neon.tech/)
2. Click "Create Project"
3. Name: `hackathon-todo-phase2`
4. Region: Choose nearest to you
5. Copy the connection string (looks like: `postgresql://user:password@ep-xxx.us-east-2.aws.neon.tech/neondb`)

### Step 2: Configure Backend Environment

Create `backend/.env` from template:

```bash
# Database Connection
DATABASE_URL=postgresql+asyncpg://user:password@ep-xxx.us-east-2.aws.neon.tech/neondb

# JWT Configuration (MUST match frontend)
JWT_SECRET=your-super-secret-jwt-key-minimum-32-characters-long
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# CORS (allow frontend origin)
ALLOWED_ORIGINS=http://localhost:3000,http://frontend:3000

# Server Configuration
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=info

# Environment
ENVIRONMENT=development
```

**Important Notes**:
- Replace `DATABASE_URL` with your Neon connection string
- Change protocol from `postgresql://` to `postgresql+asyncpg://` (required for async)
- Generate secure `JWT_SECRET`: `openssl rand -base64 32`
- **NEVER** commit `.env` file to git (already in `.gitignore`)

### Step 3: Configure Frontend Environment

Create `frontend/.env.local` from template:

```bash
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# Better Auth Configuration
BETTER_AUTH_SECRET=your-super-secret-jwt-key-minimum-32-characters-long
BETTER_AUTH_URL=http://localhost:3000

# Environment
NEXT_PUBLIC_ENVIRONMENT=development
```

**Important Notes**:
- `BETTER_AUTH_SECRET` MUST match `JWT_SECRET` in backend/.env
- `NEXT_PUBLIC_*` variables are embedded in client-side code (safe for public values only)
- `.env.local` is already in `.gitignore`

### Step 4: Verify Configuration

```bash
# Check backend .env
cat backend/.env | grep -v "^#" | grep .

# Check frontend .env.local
cat frontend/.env.local | grep -v "^#" | grep .
```

Ensure no placeholder values like `<your-value-here>` remain.

---

## Running with Docker Compose

### Start All Services

```bash
# From repository root
docker-compose up --build

# Or run in background (detached)
docker-compose up -d --build
```

**Services Started**:
- `backend`: FastAPI server on port 8000
- `frontend`: Next.js app on port 3000

**Logs**:
```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Run Database Migrations

**First time only** (creates `tasks` table):

```bash
docker-compose exec backend alembic upgrade head
```

**After modifying models** (create new migration):

```bash
docker-compose exec backend alembic revision --autogenerate -m "description"
docker-compose exec backend alembic upgrade head
```

### Stop Services

```bash
# Stop but keep containers
docker-compose stop

# Stop and remove containers (preserves volumes)
docker-compose down

# Stop, remove containers AND volumes (deletes data)
docker-compose down -v
```

### Access Services

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation** (Swagger): http://localhost:8000/docs
- **API Documentation** (ReDoc): http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

---

## Running Services Locally (Without Docker)

Useful for debugging, faster iteration, or IDE integration.

### Backend (FastAPI)

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Start backend server with auto-reload
uvicorn main:app --reload --port 8000 --host 0.0.0.0

# Backend running at: http://localhost:8000
```

**Development Commands**:
```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=src --cov-report=html

# Lint code
ruff check src/

# Format code
ruff format src/

# Type check
mypy src/
```

### Frontend (Next.js)

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server with hot reload
npm run dev

# Frontend running at: http://localhost:3000
```

**Development Commands**:
```bash
# Run tests
npm test

# Run tests in watch mode
npm test -- --watch

# Lint code
npm run lint

# Type check
npm run type-check

# Build for production
npm run build

# Start production server
npm start
```

---

## User Flow Testing

### 1. Sign Up (Create Account)

1. Navigate to http://localhost:3000
2. Click "Sign Up" button
3. Fill form:
   - Email: `test@example.com`
   - Password: `SecurePassword123!`
4. Submit form
5. **Expected**: Redirected to `/tasks` page, JWT token stored in httpOnly cookie

**Verify**:
- Check browser DevTools → Application → Cookies → `better-auth-token`
- Token should be httpOnly (not accessible via JavaScript)

### 2. Login (Existing User)

1. Navigate to http://localhost:3000/login
2. Enter credentials:
   - Email: `test@example.com`
   - Password: `SecurePassword123!`
3. Submit form
4. **Expected**: Redirected to `/tasks`, JWT token refreshed

### 3. Create Task

1. On `/tasks` page, find "New Task" button
2. Click to open create form
3. Fill form:
   - Title: `Buy groceries`
   - Description: `Milk, bread, eggs` (optional)
4. Submit
5. **Expected**:
   - POST request to `/api/tasks`
   - New task appears in list immediately (optimistic UI)
   - Task shows as incomplete (unchecked)

**Verify in Network Tab**:
```json
POST /api/tasks
Authorization: Bearer <jwt-token>
Content-Type: application/json

{
  "title": "Buy groceries",
  "description": "Milk, bread, eggs"
}

Response 201:
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
  "title": "Buy groceries",
  "description": "Milk, bread, eggs",
  "completed": false,
  "created_at": "2025-12-30T10:00:00Z",
  "updated_at": "2025-12-30T10:00:00Z"
}
```

### 4. Update Task

1. Click on a task to open detail view
2. Click "Edit" button
3. Modify title: `Buy groceries and cook dinner`
4. Modify description: `Also need vegetables`
5. Submit
6. **Expected**:
   - PUT request to `/api/tasks/{id}`
   - Task updates in list
   - `updated_at` timestamp changes

### 5. Toggle Completion

1. On task list, find checkbox next to task
2. Click checkbox
3. **Expected**:
   - PATCH request to `/api/tasks/{id}/complete`
   - Checkbox toggles immediately (optimistic UI)
   - Task moves to "Completed" section (if using sections)
   - Background color or styling changes

4. Click checkbox again
5. **Expected**:
   - Task marked as incomplete
   - Returns to "Active" section

### 6. Delete Task

1. Hover over task to reveal delete button (trash icon)
2. Click delete button
3. **Expected**: Confirmation dialog appears
4. Confirm deletion
5. **Expected**:
   - DELETE request to `/api/tasks/{id}`
   - Task removed from list immediately
   - Task soft-deleted in database (`deleted_at` set)

**Verify in Database** (optional):
```sql
SELECT id, title, deleted_at FROM tasks WHERE deleted_at IS NOT NULL;
```

### 7. User Isolation Test

1. Create second account: `user2@example.com`
2. Login as user2
3. **Expected**: No tasks visible (user1's tasks not shown)
4. Create task as user2: `User 2 Task`
5. Logout and login as user1
6. **Expected**: Only user1's tasks visible, not user2's task

**Security Test** (should fail):
```bash
# Get user1's task ID
TASK_ID="<user1-task-id>"

# Try to access as user2 (should return 403)
curl -X GET http://localhost:8000/api/tasks/$TASK_ID \
  -H "Authorization: Bearer <user2-jwt-token>"

# Expected Response:
# 403 Forbidden
# {"detail": "Not authorized to access this task"}
```

---

## Testing

### Backend Tests

```bash
# Run all backend tests
cd backend
pytest

# Run specific test file
pytest tests/test_api/test_tasks.py

# Run with coverage report
pytest --cov=src --cov-report=term-missing

# Run tests in parallel (faster)
pytest -n auto
```

**Test Types**:
- **Unit Tests**: `tests/test_services/`, `tests/test_models/`
- **Integration Tests**: `tests/test_api/`
- **Contract Tests**: Validate OpenAPI spec compliance

### Frontend Tests

```bash
# Run all frontend tests
cd frontend
npm test

# Run tests in watch mode
npm test -- --watch

# Run tests with coverage
npm test -- --coverage

# Run specific test file
npm test -- TaskList.test.tsx
```

**Test Types**:
- **Component Tests**: `__tests__/components/`
- **Integration Tests**: `__tests__/lib/`
- **E2E Tests** (if implemented): Playwright or Cypress

---

## Troubleshooting

### Problem: CORS Errors

**Symptoms**:
```
Access to fetch at 'http://localhost:8000/api/tasks' from origin 'http://localhost:3000'
has been blocked by CORS policy
```

**Solutions**:
1. Verify `ALLOWED_ORIGINS` in `backend/.env` includes `http://localhost:3000`
2. Restart backend service: `docker-compose restart backend`
3. Check FastAPI CORS middleware is configured:
   ```python
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["http://localhost:3000"],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

### Problem: JWT Verification Fails

**Symptoms**:
```
401 Unauthorized: Invalid authentication credentials
```

**Solutions**:
1. Verify `JWT_SECRET` matches in both `backend/.env` and `frontend/.env.local`
2. Check token is included in request headers (DevTools → Network → Headers)
3. Verify token format: `Authorization: Bearer <token>`
4. Check token expiration (default 24h): decode at [jwt.io](https://jwt.io/)
5. Clear cookies and re-login

### Problem: Database Connection Fails

**Symptoms**:
```
sqlalchemy.exc.OperationalError: could not connect to server
```

**Solutions**:
1. Verify `DATABASE_URL` in `backend/.env` is correct
2. Check protocol is `postgresql+asyncpg://` (not `postgresql://`)
3. Verify Neon database is running (check dashboard)
4. Check IP allowlist in Neon dashboard includes your IP (or set to `0.0.0.0/0` for dev)
5. Test connection manually:
   ```bash
   psql "postgresql://user:pass@host/db"
   ```

### Problem: Docker Hot Reload Not Working

**Symptoms**:
- Code changes not reflected without rebuild

**Solutions**:
1. Verify volume mounts in `docker-compose.yml`:
   ```yaml
   volumes:
     - ./backend:/app
     - ./frontend:/app
   ```
2. **Windows users**: Ensure Docker Desktop file sharing includes project directory
3. **macOS users**: Check Docker Desktop → Preferences → Resources → File Sharing
4. Restart Docker Desktop
5. Rebuild containers: `docker-compose up --build`

### Problem: Frontend Shows "Module not found"

**Symptoms**:
```
Module not found: Can't resolve '@/components/TaskList'
```

**Solutions**:
1. Install dependencies: `npm install`
2. Clear Next.js cache: `rm -rf .next`
3. Rebuild: `npm run dev`
4. Check `tsconfig.json` has correct path aliases:
   ```json
   {
     "compilerOptions": {
       "paths": {
         "@/*": ["./*"]
       }
     }
   }
   ```

### Problem: Backend Import Errors

**Symptoms**:
```
ModuleNotFoundError: No module named 'src'
```

**Solutions**:
1. Verify virtual environment is activated: `which python` should show `.venv/bin/python`
2. Install dependencies: `pip install -r requirements.txt`
3. Check PYTHONPATH includes project root
4. Use absolute imports: `from src.models.task import Task`

### Problem: Port Already in Use

**Symptoms**:
```
Error starting userland proxy: listen tcp 0.0.0.0:3000: bind: address already in use
```

**Solutions**:
1. Find process using port: `lsof -i :3000` (macOS/Linux) or `netstat -ano | findstr :3000` (Windows)
2. Kill process: `kill -9 <PID>`
3. Change port in `docker-compose.yml`:
   ```yaml
   frontend:
     ports:
       - "3001:3000"  # Map to different host port
   ```

---

## Additional Resources

### Documentation
- [Next.js Docs](https://nextjs.org/docs)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Better Auth Docs](https://www.better-auth.com/docs)
- [SQLModel Docs](https://sqlmodel.tiangolo.com/)
- [Neon Docs](https://neon.tech/docs)

### API Testing
- **Swagger UI**: http://localhost:8000/docs (interactive API testing)
- **ReDoc**: http://localhost:8000/redoc (API documentation)
- **OpenAPI Spec**: specs/002-phase2-fullstack-setup/contracts/api-spec.yaml

### Project Structure
- **Specifications**: `specs/002-phase2-fullstack-setup/`
- **Frontend Code**: `frontend/`
- **Backend Code**: `backend/`
- **Phase I (CLI)**: `src/`, `tests/`

### Development Workflow
1. Read feature spec: `specs/002-phase2-fullstack-setup/spec.md`
2. Review plan: `specs/002-phase2-fullstack-setup/plan.md`
3. Check tasks: `specs/002-phase2-fullstack-setup/tasks.md` (after `/sp.tasks`)
4. Backend guide: `backend/CLAUDE.md`
5. Frontend guide: `frontend/CLAUDE.md`

---

## Getting Help

**Issues**:
1. Check this troubleshooting section first
2. Review error logs: `docker-compose logs backend` or `docker-compose logs frontend`
3. Verify environment variables are set correctly
4. Test each service independently (run locally without Docker)
5. Check GitHub issues or create new issue

**Common Commands Reference**:
```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Restart specific service
docker-compose restart backend

# Rebuild after code changes
docker-compose up --build

# Run migrations
docker-compose exec backend alembic upgrade head

# Access backend shell
docker-compose exec backend bash

# Access frontend shell
docker-compose exec frontend sh

# Stop all services
docker-compose down
```

**Next Steps**:
- Review API specification: `contracts/api-spec.yaml`
- Read data model: `data-model.md`
- Check constitution: `.specify/memory/constitution.md`
- Run `/sp.tasks` to generate implementation tasks
