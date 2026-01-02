# Implementation Plan: AI-Powered Todo Chatbot (Phase III)

**Branch**: `003-ai-chatbot` | **Date**: 2025-12-31 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/003-ai-chatbot/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Transform Phase II's form-based web application into an AI-powered chatbot interface where users manage tasks through natural language conversation. Core technical approach: stateless FastAPI backend with OpenAI Agents SDK, MCP protocol for tool invocation, Next.js frontend with ChatKit UI, and PostgreSQL for conversation persistence. All conversation state stored in database to enable horizontal scaling and zero in-memory dependencies.

## Technical Context

**Language/Version**: Python 3.11+ (backend), TypeScript 5.x (frontend), Node.js 20+ (frontend runtime)
**Primary Dependencies**:
  - Backend: FastAPI 0.104+, SQLModel 0.14+, OpenAI Agents SDK (latest), Official MCP SDK (latest), Alembic 1.12+, Pydantic 2.x
  - Frontend: Next.js 16+, React 19+, OpenAI ChatKit (official package), Better Auth (existing), TypeScript 5.x, Tailwind CSS
**Storage**: Neon Serverless PostgreSQL (existing from Phase II), extended with Conversation and Message tables
**Testing**: pytest 7.x+ (backend), pytest-asyncio (async tests), Jest + React Testing Library (frontend)
**Target Platform**: Linux server (Docker containers), browser (Chrome/Firefox/Safari latest 2 versions)
**Project Type**: Web application (frontend + backend monorepo)
**Performance Goals**:
  - < 2 seconds AI response time (95th percentile)
  - 100+ concurrent chat requests without degradation
  - < 500ms database query latency
  - < 10 seconds task creation end-to-end
**Constraints**:
  - Stateless architecture (zero in-memory session state)
  - All conversation state in PostgreSQL
  - Must survive backend restart mid-conversation
  - JWT authentication preserved from Phase II
  - Docker-compatible deployment
**Scale/Scope**:
  - 100-1000 concurrent users
  - Unlimited conversation history per user
  - 5 MCP tools (task operations)
  - 1 chat API endpoint
  - 2 new database tables

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### ✅ I. Spec-Driven Development First
- All code generated from specs/003-ai-chatbot/spec.md
- MCP tools spec (mcp-tools-spec.md) defines tool contracts
- Phase III overview (phase3-overview.md) guides architecture
- No manual coding permitted

### ✅ II. Phase-Based Development Discipline
- Phase III scope strictly limited to AI chatbot feature
- Builds on Phase II (auth, database, API) without breaking it
- No Phase IV/V features (e.g., multi-language, advanced analytics)
- Backward compatible: existing REST API endpoints remain functional

### ✅ III. Documentation as Core Artifact
- Specification complete with intent, constraints, acceptance criteria
- Implementation plan (this document) captures technical approach
- API contracts defined in contracts/ directory (Phase 1 output)
- README updates planned for setup instructions

### ✅ IV. Reusable Intelligence & Agent Skills
- MCP tools designed for reusability across AI systems
- Tool protocol follows Official MCP SDK standards
- No custom skills needed initially (< 3 repetitions)
- Future: Consider skill for "chat endpoint + tool orchestration" pattern

### ✅ V. AI Agent Governance
- OpenAI Agents SDK provides scoped agent execution
- System prompt defines agent behavior boundaries
- Agent outputs auditable via conversation message log
- Tool invocations recorded in database for traceability

### ✅ VI. Code Quality Standards
- Production-ready error handling (graceful degradation when AI fails)
- Input validation on all user messages and tool parameters
- Logging for debugging (conversation_id, user_id, tool calls)
- Secure: JWT auth, parameterized queries, no secrets in code

### ✅ VII. Security & Privacy
- JWT authentication enforced on chat endpoint
- All tool operations scoped to authenticated user_id
- No cross-user data leaks (user_id filtering in all DB queries)
- Environment variables for OpenAI API key (not hardcoded)
- SQL injection prevention via SQLModel ORM

### ✅ VIII. Cloud-Native Readiness
- Stateless design enables horizontal scaling
- Docker Compose configuration extended for Phase III
- Health check endpoint for Kubernetes (future)
- Database connection pooling for multi-instance deployment
- 12-factor app principles (config via environment)

### ✅ IX. Performance & Token Efficiency
- Conversation history windowing to limit context size
- Minimal system prompt (clear but concise)
- MCP tools return only necessary data
- Database indexes on user_id, conversation_id for fast queries
- Async/await for I/O operations (FastAPI async routes)

**Gate Status**: ✅ PASS - No constitution violations

## Project Structure

### Documentation (this feature)

```text
specs/003-ai-chatbot/
├── spec.md              # Feature specification (completed)
├── phase3-overview.md   # Architecture overview (completed)
├── mcp-tools-spec.md    # MCP tools specification (completed)
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command - pending)
├── data-model.md        # Phase 1 output (/sp.plan command - pending)
├── quickstart.md        # Phase 1 output (/sp.plan command - pending)
├── contracts/           # Phase 1 output (/sp.plan command - pending)
│   ├── chat-api.yaml    # OpenAPI spec for chat endpoint
│   └── mcp-tools.json   # MCP tool schemas (JSON Schema)
├── checklists/
│   └── requirements.md  # Spec quality checklist (completed)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── models/
│   ├── __init__.py
│   ├── task.py              # Existing from Phase II
│   ├── user.py              # Existing from Phase II
│   ├── conversation.py      # NEW: Conversation model
│   └── message.py           # NEW: Message model
├── mcp_tools/               # NEW: MCP tools directory
│   ├── __init__.py
│   ├── task_tools.py        # 5 MCP tools implementation
│   ├── schemas.py           # JSON schemas for tools
│   └── README.md            # Tool documentation
├── routers/
│   ├── tasks.py             # Existing from Phase II
│   ├── auth.py              # Existing from Phase II
│   └── chat.py              # NEW: Chat endpoint
├── services/
│   ├── agent_service.py     # NEW: OpenAI Agents SDK integration
│   └── conversation_service.py  # NEW: Conversation management
├── tests/
│   ├── test_tasks.py        # Existing from Phase II
│   ├── test_mcp_tools.py    # NEW: MCP tools unit tests
│   ├── test_chat_endpoint.py  # NEW: Chat API integration tests
│   └── test_agent_service.py  # NEW: Agent behavior tests
├── alembic/
│   └── versions/
│       ├── xxx_add_conversations.py  # NEW: Conversation table migration
│       └── xxx_add_messages.py       # NEW: Message table migration
├── main.py                  # Extended with chat router
├── requirements.txt         # Updated with new dependencies
└── README.md                # Updated with Phase III setup

frontend/
├── src/
│   ├── app/
│   │   ├── chat/
│   │   │   └── page.tsx     # NEW: Chat page
│   │   ├── tasks/           # Existing from Phase II
│   │   └── layout.tsx       # Existing from Phase II
│   ├── components/
│   │   ├── ChatInterface.tsx  # NEW: ChatKit wrapper
│   │   ├── MessageList.tsx    # NEW: Message display
│   │   └── ChatInput.tsx      # NEW: User input component
│   └── lib/
│       └── chat-api.ts      # NEW: Chat API client
├── tests/
│   └── chat.test.tsx        # NEW: Chat UI tests
├── package.json             # Updated with ChatKit dependency
└── README.md                # Updated with Phase III frontend setup

docker-compose.yml           # Extended for Phase III services
.env.example                 # Updated with OpenAI API key
README.md                    # Updated with Phase III overview
```

**Structure Decision**: Web application (Option 2) - existing monorepo from Phase II extended with AI chatbot components. Backend adds MCP tools, chat endpoint, agent service, and conversation models. Frontend adds ChatKit UI and chat page. Database extends with 2 new tables (conversations, messages).

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations - Constitution Check passed. No complexity tracking needed.

---

## Phase 0: Research & Technical Discovery

**Objective**: Resolve unknowns and validate technology choices for OpenAI Agents SDK + MCP integration

### Research Tasks

1. **OpenAI Agents SDK Integration**
   - Research: How to instantiate and configure OpenAI Agent
   - Research: System prompt best practices for task management
   - Research: Agent response streaming vs. blocking
   - Research: Error handling when AI service unavailable
   - **Decision needed**: Agent initialization pattern (per-request vs. singleton)

2. **Official MCP SDK Usage**
   - Research: MCP tool registration process
   - Research: Tool schema definition (JSON Schema format)
   - Research: Stateless tool design patterns
   - Research: Tool error propagation to agent
   - **Decision needed**: MCP server lifecycle (per-request vs. application-wide)

3. **OpenAI ChatKit Frontend Integration**
   - Research: ChatKit installation and setup for Next.js 16
   - Research: ChatKit customization options (styling, behavior)
   - Research: Authentication flow integration with Better Auth
   - Research: Message history rendering from database
   - **Decision needed**: ChatKit vs. custom React components

4. **Stateless Architecture Validation**
   - Research: FastAPI async patterns for DB + AI SDK
   - Research: Connection pooling for Neon PostgreSQL
   - Research: Transaction isolation for concurrent messages
   - Research: Conversation history windowing strategies
   - **Decision needed**: Max conversation history length (token budget)

5. **Database Performance**
   - Research: Index strategies for conversation queries
   - Research: Message table partitioning by user_id
   - Research: PostgreSQL full-text search for message content (future)
   - **Decision needed**: Conversation history retention policy

### Unknowns to Resolve

| Unknown | Research Question | Output |
|---------|-------------------|--------|
| Agent Initialization | Create agent per-request or reuse singleton? | Pattern + code example |
| MCP Tool Registration | Register tools at startup or per-request? | Registration code pattern |
| ChatKit Setup | Production domain allowlist process | Setup steps + ENV vars |
| Conversation Windowing | How many messages to include in context? | Token budget calculation |
| Error Handling | Fallback when OpenAI API fails? | Error response pattern |

**Output**: research.md document with decisions, rationales, and code patterns

---

## Phase 1: Design & Data Modeling

**Prerequisites**: research.md complete

### 1.1 Data Model Design

**Output**: data-model.md

**Entities**:

**Conversation**:
```python
class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    messages: List["Message"] = Relationship(back_populates="conversation")

    # Indexes
    __table_args__ = (
        Index("ix_conversations_user_id_created", "user_id", "created_at"),
    )
```

**Message**:
```python
class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversations.id", index=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    role: str = Field(sa_column=Column(Enum("user", "assistant", name="message_role")))
    content: str = Field(sa_column=Column(Text))
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    conversation: Optional[Conversation] = Relationship(back_populates="messages")

    # Indexes
    __table_args__ = (
        Index("ix_messages_conversation_id_created", "conversation_id", "created_at"),
        Index("ix_messages_user_id_conversation_id", "user_id", "conversation_id"),
    )
```

**Task** (existing, no changes):
- Reused from Phase II without modification
- Already has user_id, title, description, status, created_at, completed_at

**Validation Rules**:
- Conversation: user_id must reference existing user
- Message: role must be "user" or "assistant"
- Message: content max length 10,000 characters
- Message: conversation_id must reference existing conversation

**State Transitions**: N/A (no complex state machines)

### 1.2 API Contracts

**Output**: contracts/chat-api.yaml (OpenAPI 3.0)

**Endpoint**: POST /api/{user_id}/chat

```yaml
openapi: 3.0.3
info:
  title: Chat API
  version: 1.0.0
paths:
  /api/{user_id}/chat:
    post:
      summary: Send message to AI chatbot
      security:
        - BearerAuth: []
      parameters:
        - name: user_id
          in: path
          required: true
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                conversation_id:
                  type: integer
                  nullable: true
                  description: Optional - creates new conversation if omitted
                message:
                  type: string
                  maxLength: 1000
                  description: User message
              required:
                - message
      responses:
        200:
          description: Successful response
          content:
            application/json:
              schema:
                type: object
                properties:
                  conversation_id:
                    type: integer
                  response:
                    type: string
                  tool_calls:
                    type: array
                    items:
                      type: object
                      properties:
                        tool:
                          type: string
                        parameters:
                          type: object
                        result:
                          type: object
        401:
          description: Unauthorized (invalid JWT)
        429:
          description: Rate limit exceeded
        500:
          description: AI service unavailable
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
```

**MCP Tool Contracts**: See contracts/mcp-tools.json for full JSON Schema definitions

**Tool: add_task**:
```json
{
  "name": "add_task",
  "description": "Create a new task for the user",
  "inputSchema": {
    "type": "object",
    "properties": {
      "user_id": {"type": "string"},
      "title": {"type": "string", "maxLength": 200},
      "description": {"type": "string", "maxLength": 1000}
    },
    "required": ["user_id", "title"]
  },
  "outputSchema": {
    "type": "object",
    "properties": {
      "task_id": {"type": "integer"},
      "status": {"type": "string", "enum": ["created"]},
      "title": {"type": "string"}
    }
  }
}
```

Similar schemas for: get_tasks, update_task_status, delete_task, get_task_statistics

### 1.3 Quickstart Guide

**Output**: quickstart.md

Local development setup:
1. Install dependencies: `pip install -r backend/requirements.txt && npm install --prefix frontend`
2. Set environment variables: Copy `.env.example` to `.env` and fill in OpenAI API key
3. Run migrations: `alembic upgrade head`
4. Start backend: `uvicorn main:app --reload --port 8000`
5. Start frontend: `npm run dev --prefix frontend`
6. Open http://localhost:3000/chat
7. Test: Send message "Add a task to buy groceries" and verify task created

Production deployment:
1. Deploy to cloud (Vercel frontend + Render/Railway backend)
2. Add frontend domain to OpenAI allowlist
3. Set NEXT_PUBLIC_OPENAI_DOMAIN_KEY
4. Run migrations on production database
5. Verify health check endpoints

---

## Phase 2 Planning Complete

**Status**: Implementation plan ready for `/sp.tasks`

**Next Steps**:
1. Review research.md decisions
2. Validate data-model.md entity designs
3. Review API contracts in contracts/
4. Run `/sp.tasks` to generate actionable task breakdown

**Deliverables Created**:
- ✅ plan.md (this file)
- ⏳ research.md (generated in Phase 0)
- ⏳ data-model.md (generated in Phase 1)
- ⏳ contracts/chat-api.yaml (generated in Phase 1)
- ⏳ contracts/mcp-tools.json (generated in Phase 1)
- ⏳ quickstart.md (generated in Phase 1)

**Branch**: 003-ai-chatbot
**Spec**: specs/003-ai-chatbot/spec.md
**Plan**: specs/003-ai-chatbot/plan.md

---

**Note**: This plan follows spec-driven development principles. All code will be generated from these specifications using Claude Code. No manual coding permitted per Constitution Principle I.
