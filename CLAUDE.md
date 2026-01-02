# Hackathon Todo - Phase II: Full-Stack Web Application

## Project Overview
Multi-user web application with authentication, built using spec-driven development.

## Spec-Kit Structure
All specifications in `/specs`:
- `overview.md` - Project overview
- `features/` - Feature specifications
- `api/` - API endpoint specs
- `database/` - Schema specs
- `ui/` - Component specs

## Monorepo Layout
- `/frontend` - Next.js 16+ app (TypeScript, Tailwind)
- `/backend` - FastAPI server (Python, SQLModel)
- `/specs` - Spec-Kit specifications

## Development Workflow
1. Read spec: @specs/features/[feature].md
2. Backend: @backend/CLAUDE.md
3. Frontend: @frontend/CLAUDE.md
4. Test integration

## Key Technologies
- **Frontend**: Next.js 16 App Router, Better Auth, TypeScript
- **Backend**: FastAPI, SQLModel, JWT verification
- **Database**: Neon Serverless PostgreSQL
- **Auth**: Better Auth + JWT tokens

## Running the Application
```bash
# Backend
cd backend && uvicorn main:app --reload --port 8000

# Frontend
cd frontend && npm run dev

# Or both with Docker
docker-compose up
```

## Authentication Flow
1. User login → Better Auth issues JWT
2. Frontend stores JWT
3. Every API call includes: `Authorization: Bearer <token>`
4. Backend verifies JWT and filters by user_id

## Important Notes
- All development via Claude Code (no manual coding)
- Follow TDD approach
- Document all iterations in specs/
- Update PHR after each major step

## Active Technologies
- Python 3.11+ (backend), TypeScript 5.x (frontend), Node.js 20+ (frontend runtime) (003-ai-chatbot)
- Neon Serverless PostgreSQL (existing from Phase II), extended with Conversation and Message tables (003-ai-chatbot)

## Recent Changes
- 003-ai-chatbot: Added Python 3.11+ (backend), TypeScript 5.x (frontend), Node.js 20+ (frontend runtime)
