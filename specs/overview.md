# Todo Application - Phase II Overview

## Current Phase
**Phase II: Full-Stack Web Application**

## Objective
Transform CLI console app into modern web application with:
- Multi-user support
- Authentication
- Persistent database storage
- RESTful API
- Responsive web UI

## Architecture

### Frontend
- **Framework**: Next.js 16+ with App Router
- **Language**: TypeScript (strict mode)
- **Styling**: Tailwind CSS
- **Authentication**: Better Auth client integration
- **Features**:
  - Server components by default
  - Client components only when interactive
  - Optimistic UI updates
  - Form validation with react-hook-form

### Backend
- **Framework**: FastAPI (Python)
- **ORM**: SQLModel
- **Authentication**: JWT verification (from Better Auth)
- **Features**:
  - RESTful API endpoints
  - User-scoped data filtering
  - Pydantic validation
  - Async request handling

### Database
- **Provider**: Neon Serverless PostgreSQL
- **Schema**:
  - `users` table (managed by Better Auth)
  - `tasks` table with user_id foreign key
- **Migrations**: Alembic
- **Indexes**: user_id, created_at

## User Flow

### 1. Authentication
1. User visits app → redirected to login
2. Better Auth handles registration/login
3. JWT token stored in httpOnly cookie
4. Token included in all API requests

### 2. Task Management
1. User views personal task list (GET /api/tasks)
2. Creates new task (POST /api/tasks)
3. Updates task status (PUT /api/tasks/{id})
4. Deletes task (DELETE /api/tasks/{id})

### 3. Data Isolation
- Every API call verified with JWT
- Backend filters all queries by user_id
- Users only see their own tasks

## API Endpoints

All endpoints require `Authorization: Bearer <token>` header:

1. `GET /api/tasks` - List user's tasks
2. `POST /api/tasks` - Create new task
3. `GET /api/tasks/{id}` - Get single task
4. `PUT /api/tasks/{id}` - Update task
5. `DELETE /api/tasks/{id}` - Delete task
6. `PATCH /api/tasks/{id}/complete` - Toggle completion

## Development Phases

### Feature Breakdown (Priority Order)
1. **Authentication** (P1)
   - Better Auth setup
   - JWT verification middleware
   - User session management

2. **Database Setup** (P1)
   - Neon PostgreSQL connection
   - Schema migrations
   - SQLModel models

3. **Task CRUD API** (P2)
   - All 6 REST endpoints
   - User data filtering
   - Error handling

4. **Task CRUD UI** (P2)
   - Task list component
   - Create/edit forms
   - Delete confirmation
   - Optimistic updates

## Success Criteria

### Authentication
- [x] Better Auth integrated and working
- [x] JWT tokens issued on login
- [x] Backend verifies JWT on every request
- [x] Unauthorized requests rejected with 401

### Task Management
- [x] Users can CRUD their own tasks
- [x] Users cannot see other users' tasks
- [x] Task completion can be toggled
- [x] All operations persist to database

### API Quality
- [x] All 6 endpoints functional
- [x] Proper HTTP status codes
- [x] Request validation with Pydantic
- [x] Error responses include helpful messages

### Frontend Quality
- [x] Responsive design (mobile + desktop)
- [x] Loading states during API calls
- [x] Error states displayed to user
- [x] Optimistic UI for instant feedback

### Security
- [x] No hardcoded secrets (use .env)
- [x] SQL injection prevented (SQLModel ORM)
- [x] XSS prevented (Next.js auto-escaping)
- [x] CORS configured correctly

### DevOps
- [x] Backend runs via `uvicorn main:app --reload`
- [x] Frontend runs via `npm run dev`
- [x] Database migrations documented
- [x] Environment setup instructions in README

## Related Specifications

- `features/authentication.md` - Auth flow details
- `features/task-crud-api.md` - API specifications
- `features/task-crud-ui.md` - Frontend components
- `features/database-setup.md` - Schema and migrations
- `api/` - Individual endpoint specs
- `database/` - Schema definitions
- `ui/` - Component specifications

## References

- Phase I (CLI app): `specs/001-in-memory-todo/`
- Constitution: `.specify/memory/constitution.md`
- Config: `.spec-kit/config.yaml`
