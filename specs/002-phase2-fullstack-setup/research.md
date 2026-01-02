# Research: Phase II Full-Stack Web Application Setup

**Date**: 2025-12-30
**Purpose**: Resolve technical unknowns and validate technology choices before design phase

## 1. Better Auth + Next.js 16 Integration

### Decision
Use Better Auth with JWT plugin, httpOnly cookies for token storage, and Next.js 16 App Router with server components for authentication.

### Rationale
- **Security**: httpOnly cookies prevent XSS attacks (JavaScript cannot access tokens)
- **SSR Compatibility**: Better Auth works seamlessly with Next.js App Router and server components
- **Built-in Session Management**: Handles token refresh, expiration, and user session automatically
- **TypeScript Support**: Full type safety for auth state and user objects
- **Minimal Setup**: Less configuration than NextAuth.js, more flexible than Clerk

### Alternatives Considered
1. **NextAuth.js**: More mature but complex configuration, opinionated providers
2. **Clerk**: Proprietary, paid tiers required for production, vendor lock-in
3. **Custom JWT Implementation**: Reinventing the wheel, prone to security vulnerabilities
4. **Supabase Auth**: Ties to Supabase ecosystem, not standalone

### Implementation Notes
- Install: `npm install better-auth @better-auth/jwt`
- Configuration in `app/lib/auth.ts` with JWT secret from environment
- Auth provider wraps root layout for global session access
- Protected routes use middleware to check session before rendering
- Token automatically included in API requests via interceptor

**References**:
- Better Auth Docs: https://www.better-auth.com/docs
- Next.js 16 Auth Patterns: https://nextjs.org/docs/app/building-your-application/authentication

---

## 2. FastAPI + SQLModel + Async PostgreSQL

### Decision
Use SQLModel with async SQLAlchemy engine and asyncpg driver for Neon PostgreSQL, with FastAPI dependency injection for database sessions.

### Rationale
- **Type Safety**: SQLModel combines Pydantic models with SQLAlchemy ORM for full type checking
- **Performance**: Async engine handles concurrent requests efficiently without blocking
- **Simplicity**: Single model definition serves as both Pydantic schema and database table
- **Validation**: Built-in Pydantic validation for all database operations
- **Compatibility**: SQLModel is built on SQLAlchemy, so Alembic migrations work seamlessly

### Alternatives Considered
1. **Raw SQLAlchemy**: More verbose, requires separate Pydantic models for validation
2. **Tortoise ORM**: Less mature ecosystem, fewer integrations
3. **Peewee**: Synchronous only, not suitable for async FastAPI
4. **Django ORM**: Overkill, requires full Django framework

### Implementation Notes
- Database URL format: `postgresql+asyncpg://user:pass@host/db`
- Create async engine with `create_async_engine(DATABASE_URL)`
- Use `AsyncSession` for all database operations
- Dependency injection pattern:
  ```python
  async def get_session() -> AsyncGenerator[AsyncSession, None]:
      async with AsyncSessionLocal() as session:
          yield session

  @app.get("/api/tasks")
  async def get_tasks(session: AsyncSession = Depends(get_session)):
      ...
  ```
- Connection pooling handled automatically by SQLAlchemy

**References**:
- SQLModel Docs: https://sqlmodel.tiangolo.com/
- FastAPI Async SQL: https://fastapi.tiangolo.com/advanced/async-sql-databases/
- asyncpg: https://github.com/MagicStack/asyncpg

---

## 3. JWT Shared Secret Between Frontend and Backend

### Decision
Use a single shared secret (`JWT_SECRET`) stored in environment variables for both Better Auth token generation and FastAPI token verification, with HS256 algorithm.

### Rationale
- **Simplicity**: Single secret is easiest to manage for MVP/hackathon
- **Security**: Sufficient for symmetric encryption when secret is properly secured
- **No Key Distribution**: Avoids complexity of public/private key pairs
- **Environment-Based**: Follows 12-factor app principles (config in environment)
- **Compatibility**: Both Better Auth and PyJWT support HS256 with shared secret

### Alternatives Considered
1. **Asymmetric Keys (RS256)**: Public/private keypair - more complex, overkill for single backend
2. **OAuth 2.0**: Separate authorization server - adds significant complexity
3. **API Gateway**: Centralized token management - requires additional infrastructure
4. **Session Cookies**: Backend stores session state - violates stateless principle

### Implementation Notes
- Generate strong secret: `openssl rand -base64 32`
- Store in `.env` files:
  - Backend: `JWT_SECRET=<secret>`
  - Frontend: `BETTER_AUTH_SECRET=<same-secret>`
- Never commit secrets to git (.env in .gitignore)
- Use `.env.example` files with placeholder values for documentation
- Token verification in FastAPI middleware:
  ```python
  import jwt
  from fastapi import Security, HTTPException
  from fastapi.security import HTTPBearer

  security = HTTPBearer()

  async def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
      token = credentials.credentials
      try:
          payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
          return payload["user_id"]
      except jwt.ExpiredSignatureError:
          raise HTTPException(401, "Token expired")
      except jwt.InvalidTokenError:
          raise HTTPException(401, "Invalid token")
  ```

**References**:
- JWT.io: https://jwt.io/
- PyJWT Docs: https://pyjwt.readthedocs.io/
- Better Auth JWT Plugin: https://www.better-auth.com/docs/plugins/jwt

---

## 4. Monorepo Tooling and Development Workflow

### Decision
Use Docker Compose for multi-service orchestration with separate containers for frontend, backend, and dev workflow. No additional monorepo tools (Turborepo, Nx, etc.).

### Rationale
- **Simplicity**: Docker Compose is sufficient for 2 services, no need for complex tooling
- **Production Parity**: Same containers used in dev and production
- **Isolated Environments**: Each service has its own dependencies and runtime
- **Easy Onboarding**: Single `docker-compose up` command starts entire stack
- **Hot Reload**: Volume mounts enable live code updates without rebuilding

### Alternatives Considered
1. **Turborepo**: Adds build caching and task orchestration - overkill for 2 services
2. **Nx**: Full-featured monorepo tool - unnecessary complexity for hackathon
3. **Manual Service Management**: Run frontend/backend separately - error-prone, inconsistent environments
4. **Kubernetes (local)**: Minikube/Kind - too heavy for local dev, save for production

### Implementation Notes
- **docker-compose.yml** structure:
  ```yaml
  version: '3.8'
  services:
    backend:
      build: ./backend
      ports:
        - "8000:8000"
      volumes:
        - ./backend:/app
      env_file:
        - ./backend/.env
      command: uvicorn main:app --host 0.0.0.0 --reload

    frontend:
      build: ./frontend
      ports:
        - "3000:3000"
      volumes:
        - ./frontend:/app
        - /app/node_modules
      env_file:
        - ./frontend/.env.local
      command: npm run dev
  ```
- **CORS Configuration** (backend FastAPI):
  ```python
  from fastapi.middleware.cors import CORSMiddleware

  app.add_middleware(
      CORSMiddleware,
      allow_origins=["http://localhost:3000"],
      allow_credentials=True,
      allow_methods=["*"],
      allow_headers=["*"],
  )
  ```
- **Port Allocation**:
  - Frontend: 3000 (Next.js default)
  - Backend: 8000 (FastAPI/Uvicorn default)
  - PostgreSQL: External (Neon cloud)

**References**:
- Docker Compose Docs: https://docs.docker.com/compose/
- FastAPI CORS: https://fastapi.tiangolo.com/tutorial/cors/

---

## 5. Database Schema Design Patterns

### Decision
Use two-table schema: `users` (Better Auth managed) and `tasks` (custom) with foreign key relationship. Implement soft deletes, composite indexes, and user-scoped queries.

### Rationale
- **Clear Ownership**: Every task explicitly belongs to one user via `user_id` foreign key
- **Efficient Filtering**: Composite index on `(user_id, created_at)` optimizes paginated queries
- **Data Integrity**: Foreign key constraint ensures referential integrity
- **Audit Trail**: Soft deletes preserve historical data (`deleted_at` timestamp)
- **Better Auth Compatibility**: Don't modify `users` table structure (managed by auth library)

### Alternatives Considered
1. **Embedded Documents**: Store tasks as JSON array in user record - not relational, poor query performance
2. **Multi-Tenancy Schema**: Separate schema per user - massive overkill, hard to manage
3. **Polymorphic Relationships**: Generic entity table - overly complex for simple use case
4. **Hard Deletes**: Permanent deletion - loses audit trail, can't recover mistakes

### Implementation Notes
- **Users Table** (Better Auth managed - reference only):
  ```sql
  CREATE TABLE users (
      id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
      email VARCHAR(255) UNIQUE NOT NULL,
      password_hash VARCHAR(255) NOT NULL,
      created_at TIMESTAMP DEFAULT NOW(),
      updated_at TIMESTAMP DEFAULT NOW()
  );
  ```

- **Tasks Table** (custom):
  ```sql
  CREATE TABLE tasks (
      id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
      user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
      title VARCHAR(200) NOT NULL CHECK (length(title) >= 1),
      description TEXT,
      completed BOOLEAN DEFAULT FALSE,
      created_at TIMESTAMP DEFAULT NOW(),
      updated_at TIMESTAMP DEFAULT NOW(),
      deleted_at TIMESTAMP NULL
  );

  -- Indexes
  CREATE INDEX idx_tasks_user_id ON tasks(user_id);
  CREATE INDEX idx_tasks_user_created ON tasks(user_id, created_at DESC);
  CREATE INDEX idx_tasks_deleted ON tasks(deleted_at) WHERE deleted_at IS NOT NULL;
  ```

- **User-Scoped Queries** (enforce in application):
  ```python
  # Always filter by user_id from JWT
  async def get_user_tasks(user_id: UUID, session: AsyncSession):
      result = await session.execute(
          select(Task)
          .where(Task.user_id == user_id)
          .where(Task.deleted_at.is_(None))
          .order_by(Task.created_at.desc())
      )
      return result.scalars().all()
  ```

- **Soft Delete Pattern**:
  ```python
  async def soft_delete_task(task_id: UUID, user_id: UUID, session: AsyncSession):
      task = await session.get(Task, task_id)
      if task.user_id != user_id:
          raise PermissionError("Not authorized")
      task.deleted_at = datetime.utcnow()
      await session.commit()
  ```

**References**:
- PostgreSQL Indexes: https://www.postgresql.org/docs/current/indexes.html
- SQLModel Relationships: https://sqlmodel.tiangolo.com/tutorial/relationship-attributes/
- Soft Deletes Pattern: https://brandur.org/soft-deletion

---

## Summary of Key Decisions

| Area | Decision | Primary Rationale |
|------|----------|-------------------|
| **Frontend Auth** | Better Auth + httpOnly cookies | Security (XSS-proof), SSR compatibility |
| **Backend ORM** | SQLModel with async engine | Type safety, validation, async performance |
| **JWT Strategy** | Shared secret (HS256) | Simplicity, sufficient security for MVP |
| **Development** | Docker Compose | Production parity, easy onboarding |
| **Database Schema** | Two-table with FK + soft deletes | Clear ownership, data integrity, audit trail |

All decisions prioritize:
1. **Security**: httpOnly cookies, JWT verification, user isolation
2. **Developer Experience**: Type safety, hot reload, single command startup
3. **Production Readiness**: Migration support, indexes, error handling
4. **Simplicity**: Avoid over-engineering, choose proven patterns

**Status**: All technical unknowns resolved. Ready for Phase 1 (Design & Contracts).
