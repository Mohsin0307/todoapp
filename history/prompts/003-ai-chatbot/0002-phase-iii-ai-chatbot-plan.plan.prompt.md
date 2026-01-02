---
id: 0002
title: phase-iii-ai-chatbot-plan
stage: plan
date: 2025-12-31
surface: claude-code
model: claude-sonnet-4-5
feature: 003-ai-chatbot
branch: 003-ai-chatbot
user: Mirza Mohsin Baig
command: /sp.plan
labels: [phase-iii, implementation-plan, openai-agents, mcp-tools, stateless-architecture]
links:
  spec: specs/003-ai-chatbot/spec.md
  ticket: N/A
  adr: N/A
  pr: N/A
files:
  - path: specs/003-ai-chatbot/plan.md
    action: created
    status: success
  - path: specs/003-ai-chatbot/research.md
    action: created
    status: success
  - path: specs/003-ai-chatbot/data-model.md
    action: created
    status: success
  - path: specs/003-ai-chatbot/contracts/chat-api.yaml
    action: created
    status: success
  - path: specs/003-ai-chatbot/contracts/mcp-tools.json
    action: created
    status: success
  - path: specs/003-ai-chatbot/quickstart.md
    action: created
    status: success
  - path: CLAUDE.md
    action: updated
    status: success
tests: []
---

## Prompt

User requested comprehensive implementation plan for Phase III: AI-Powered Todo Chatbot with detailed context:

**Project Context**:
- Phase I: CLI console app (completed)
- Phase II: Full-stack web app with auth, REST API, PostgreSQL (completed)
- Phase III Goal: Transform to AI chatbot with natural language interface

**Technology Stack Specified**:
- Frontend: OpenAI ChatKit (official chat UI), Next.js 16+
- Backend: OpenAI Agents SDK, Official MCP SDK, FastAPI
- Architecture: Stateless server (zero in-memory state, all conversation history in database)

**Core Requirements**:
1. Stateless architecture (can restart server mid-conversation)
2. MCP (Model Context Protocol) with 5 tools (add_task, get_tasks, update_task_status, delete_task, get_task_statistics)
3. Database schema extensions (Conversation and Message models)
4. Chat API endpoint (POST /api/{user_id}/chat)
5. Agent behavior with natural language understanding
6. ChatKit integration with domain allowlist setup

**Detailed Specifications Provided**:
- Database schema with SQLModel definitions
- MCP tool specifications with JSON schemas
- Request flow (11-step stateless cycle)
- Agent system prompt requirements
- Natural language understanding examples
- Error handling patterns
- Conversation windowing strategy (last 50 messages)
- Performance goals (<2s response time, 100 concurrent requests)

## Response snapshot

**Actions Taken**:

### Phase 0: Research & Technical Discovery

Created comprehensive research.md resolving all technical unknowns:

1. **OpenAI Agents SDK Integration**: Decided on per-request agent instantiation (aligns with stateless architecture)
2. **MCP Tool Registration**: Register at application startup (one-time overhead, tools are stateless)
3. **ChatKit Integration**: Use official OpenAI ChatKit (faster implementation, best practices)
4. **Conversation Windowing**: Last 50 messages (5,000 tokens + 700 for system/tools = ~5,700 total context)
5. **Error Handling**: Graceful fallback with retry logic using tenacity library

**Technology Stack Finalized**:
- Backend: FastAPI 0.104+, SQLModel 0.14+, OpenAI Agents SDK, Official MCP SDK, Alembic 1.12+, Pydantic 2.x, tenacity
- Frontend: Next.js 16+, React 19+, OpenAI ChatKit, Better Auth, TypeScript 5.x, Tailwind CSS

### Phase 1: Design & Data Modeling

**Created data-model.md** with complete entity definitions:

**Conversation Model**:
```python
- id (PK), user_id (FK), created_at, updated_at
- Indexes: (user_id, created_at) composite
- Relationships: 1:N with Message (cascade delete)
```

**Message Model**:
```python
- id (PK), conversation_id (FK), user_id (FK), role (enum: user/assistant), content (text), created_at
- Indexes: (conversation_id, created_at), (user_id, conversation_id)
- Max content length: 10,000 characters (application-level validation)
```

**Alembic Migrations**:
- Migration 1: Add conversations table
- Migration 2: Add messages table with message_role enum

**Query Patterns Defined**:
- Get user conversations: O(log n) via composite index
- Get conversation history: O(log n + 50) with DESC ordering + reverse
- Performance target: <50ms for typical queries

**Created contracts/chat-api.yaml** (OpenAPI 3.0):
- POST /api/{user_id}/chat endpoint specification
- Request/response schemas with examples
- Error responses (400, 401, 403, 404, 429, 500)
- Security: BearerAuth (JWT from Phase II)
- Rate limiting documented

**Created contracts/mcp-tools.json** (JSON Schema):
- All 5 MCP tools with complete input/output schemas
- Error cases for each tool
- Security principles (user-scoping, stateless design, error handling)
- Implementation notes (database queries, indexing, transactions, logging)

**Created quickstart.md** with complete setup guide:
- Local development (6-step setup with verification)
- Production deployment (Vercel frontend + Render backend)
- Docker deployment with health checks
- Troubleshooting section (5 common issues with solutions)
- Testing instructions (backend pytest + frontend Jest)

### Technical Context & Constitution Check

**Filled Technical Context**:
- Languages: Python 3.11+, TypeScript 5.x, Node.js 20+
- Performance: <2s AI response (95th percentile), 100+ concurrent requests
- Constraints: Stateless architecture, zero in-memory state, must survive backend restart
- Scale: 100-1000 concurrent users, unlimited conversation history

**Constitution Check**: ✅ ALL PASSED
- All 9 core principles validated
- No violations detected
- Complexity tracking: Not needed (no violations)

### Project Structure

**Documented monorepo extension**:
- Backend: +4 new modules (mcp_tools/, routers/chat.py, services/agent_service.py, services/conversation_service.py)
- Backend: +4 new test files (test_mcp_tools.py, test_chat_endpoint.py, test_agent_service.py, test_stateless.py)
- Backend: +2 Alembic migrations (conversations, messages)
- Frontend: +1 new page (app/chat/page.tsx)
- Frontend: +3 new components (ChatInterface.tsx, MessageList.tsx, ChatInput.tsx)
- Frontend: +1 API client (lib/chat-api.ts)
- Contracts: +2 API specs (chat-api.yaml, mcp-tools.json)

### Agent Context Update

Updated CLAUDE.md with:
- New languages: Python 3.11+, TypeScript 5.x, Node.js 20+
- Extended database: Neon PostgreSQL with Conversation & Message tables
- Project type confirmed: Web application (frontend + backend monorepo)

## Outcome

- ✅ Impact: Complete implementation plan created with 6 supporting documents (plan.md, research.md, data-model.md, chat-api.yaml, mcp-tools.json, quickstart.md). All technical unknowns resolved. Architecture validated as stateless and constitution-compliant. Ready for `/sp.tasks` command.
- 🧪 Tests: N/A (planning phase - test strategy defined in plan.md)
- 📁 Files: 7 files created/updated (plan.md, research.md, data-model.md, 2 contract files, quickstart.md, CLAUDE.md)
- 🔁 Next prompts: `/sp.tasks` to generate actionable task breakdown organized by user stories
- 🧠 Reflection: Plan comprehensively addresses user's detailed requirements. Stateless architecture ensures horizontal scalability. MCP tools enable reusable AI-powered task management. Phase III builds on Phase II without breaking changes. All decisions documented with rationales in research.md. Data model designed for performance with composite indexes. Quickstart provides clear path from local dev to production.

## Evaluation notes (flywheel)

- Failure modes observed: None. All specifications and requirements were clear from user input and existing Phase II context.
- Graders run and results (PASS/FAIL): Constitution Check - ALL PASSED (9/9 principles validated)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A (successful comprehensive planning on first iteration)
