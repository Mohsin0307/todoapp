# Phase 0: Research & Technical Discovery

**Feature**: AI-Powered Todo Chatbot (Phase III)
**Date**: 2025-12-31
**Status**: Complete

## Research Questions & Decisions

### 1. OpenAI Agents SDK Integration

**Question**: How should we instantiate and configure the OpenAI Agent? Per-request or singleton?

**Research Findings**:
- OpenAI Agents SDK supports both patterns
- Per-request pattern: New agent instance for each chat request
- Singleton pattern: Reuse agent instance across requests

**Decision**: **Per-request agent instantiation**

**Rationale**:
- Aligns with stateless architecture principle
- Each request is independent with its own conversation context
- Easier to implement user-scoped agents (different system prompts per user in future)
- No shared state reduces concurrency complexity
- Minimal performance overhead (agent initialization is lightweight)

**Code Pattern**:
```python
from openai_agents import Agent

async def handle_chat(user_id: str, message: str, conversation_history: List[Message]):
    # Create agent for this request
    agent = Agent(
        model="gpt-4",
        tools=mcp_tools,
        system_prompt="You are a helpful task management assistant..."
    )

    # Build context from conversation history
    messages = [{"role": msg.role, "content": msg.content} for msg in conversation_history]
    messages.append({"role": "user", "content": message})

    # Run agent
    response = await agent.run(messages)

    return response
```

**Alternatives Considered**:
- Singleton agent: Rejected due to shared state concerns and complexity of handling user-specific context

---

### 2. MCP Tool Registration

**Question**: Should we register MCP tools at application startup or per-request?

**Research Findings**:
- Official MCP SDK recommends registration at startup
- Tools are stateless functions, safe to reuse
- Registration involves schema validation (one-time cost)

**Decision**: **Register tools at application startup**

**Rationale**:
- One-time registration reduces per-request overhead
- Tools are stateless and thread-safe
- Schema validation happens once at startup (fail-fast if misconfigured)
- Consistent with FastAPI dependency injection pattern

**Code Pattern**:
```python
# backend/main.py
from mcp import MCPServer
from backend.mcp_tools.task_tools import get_task_tools

# Initialize MCP server at startup
mcp_server = MCPServer()

@app.on_event("startup")
async def startup_event():
    # Register all MCP tools
    tools = get_task_tools()
    for tool in tools:
        mcp_server.register_tool(
            name=tool.name,
            description=tool.description,
            input_schema=tool.input_schema,
            handler=tool.handler
        )

    print(f"Registered {len(tools)} MCP tools")

# Make tools available to agent in each request
def get_mcp_tools():
    return mcp_server.get_tools()
```

**Alternatives Considered**:
- Per-request registration: Rejected due to unnecessary overhead

---

### 3. OpenAI ChatKit Frontend Integration

**Question**: Should we use OpenAI ChatKit or build custom React components?

**Research Findings**:
- ChatKit provides pre-built chat UI with best practices
- Customization via props and styling
- Handles message rendering, typing indicators, input validation
- Requires domain allowlist for production
- Works with localhost without allowlist (development)

**Decision**: **Use OpenAI ChatKit for Phase III**

**Rationale**:
- Faster implementation (pre-built components)
- Follows OpenAI UI/UX best practices
- Handles edge cases (long messages, error states, loading)
- Official support and updates
- Can be replaced with custom components in future if needed

**Setup Steps**:
1. Install: `npm install @openai/chatkit`
2. Development: Works on localhost without configuration
3. Production: Add domain to https://platform.openai.com/settings/organization/security/domain-allowlist
4. Get domain key and set NEXT_PUBLIC_OPENAI_DOMAIN_KEY environment variable

**Code Pattern**:
```tsx
// frontend/src/components/ChatInterface.tsx
import { ChatKit } from '@openai/chatkit';

export function ChatInterface() {
  const handleSendMessage = async (message: string) => {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ message })
    });
    return response.json();
  };

  return (
    <ChatKit
      onSendMessage={handleSendMessage}
      placeholder="Ask me to manage your tasks..."
      className="h-full"
    />
  );
}
```

**Alternatives Considered**:
- Custom React components: Rejected for Phase III to prioritize speed. Can be reconsidered in Phase IV if customization needs exceed ChatKit capabilities.

---

### 4. Stateless Architecture & Conversation Windowing

**Question**: How many messages should we include in conversation context? What's the token budget?

**Research Findings**:
- GPT-4 context limit: 128K tokens
- Average message: ~50-100 tokens
- System prompt: ~200 tokens
- Tool definitions: ~500 tokens
- Conservative budget: Leave 50% for agent reasoning and tool outputs

**Decision**: **Include last 50 messages in conversation context**

**Rationale**:
- 50 messages × 100 tokens = 5,000 tokens
- System prompt + tools = 700 tokens
- Total context = ~5,700 tokens
- Leaves ~122,300 tokens for agent reasoning and responses
- 50 messages provides sufficient context for task management conversations
- Older conversations can be summarized if needed (future enhancement)

**Code Pattern**:
```python
# backend/services/conversation_service.py
MAX_CONVERSATION_HISTORY = 50

async def get_conversation_context(conversation_id: int) -> List[Message]:
    """Get last N messages for conversation context"""
    messages = await db.query(Message).filter(
        Message.conversation_id == conversation_id
    ).order_by(Message.created_at.desc()).limit(MAX_CONVERSATION_HISTORY).all()

    # Reverse to chronological order
    return list(reversed(messages))
```

**Alternatives Considered**:
- Include all messages: Rejected due to token budget concerns for long conversations
- Summarization of old messages: Deferred to Phase IV (adds complexity)

---

### 5. Error Handling & Graceful Degradation

**Question**: What should happen when OpenAI API fails or times out?

**Research Findings**:
- API failures can be transient (rate limits, network issues) or persistent (outages)
- User experience should degrade gracefully without losing data
- Conversation history still persisted in database

**Decision**: **Implement graceful fallback with retry logic**

**Rationale**:
- Retry once with exponential backoff for transient failures
- Fall back to helpful error message if retry fails
- User can retry manually (message already persisted)
- No data loss (conversation history intact)

**Code Pattern**:
```python
# backend/routers/chat.py
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(2), wait=wait_exponential(multiplier=1, min=1, max=5))
async def call_agent(agent, messages):
    try:
        return await agent.run(messages)
    except OpenAIAPIError as e:
        if e.status_code == 429:  # Rate limit
            raise  # Retry
        else:
            # Non-retryable error
            return {
                "response": "I'm experiencing technical difficulties right now. Please try again in a moment. Your message has been saved.",
                "tool_calls": []
            }
```

**Error Response Messages**:
- Rate limit: "I'm getting too many requests right now. Please try again in a moment."
- Timeout: "I'm taking too long to respond. Please try again."
- General failure: "I'm experiencing technical difficulties. Please try again in a moment. Your message has been saved."

**Alternatives Considered**:
- No retry logic: Rejected (poor UX for transient failures)
- Queue for background processing: Deferred to Phase IV (adds complexity)

---

### 6. Database Performance & Indexing

**Question**: What index strategies should we use for conversation queries?

**Research Findings**:
- Primary query patterns:
  1. Get all conversations for user (user_id)
  2. Get all messages for conversation (conversation_id)
  3. Get recent messages for conversation (conversation_id + created_at)
- Neon PostgreSQL supports standard B-tree indexes

**Decision**: **Composite indexes on frequently queried columns**

**Rationale**:
- Conversations: Index on (user_id, created_at) for user's conversation list
- Messages: Index on (conversation_id, created_at) for message history retrieval
- Messages: Index on (user_id, conversation_id) for user-scoped queries
- Minimal index overhead (2-3 indexes total)

**Index Strategy**:
```sql
-- Conversations table
CREATE INDEX ix_conversations_user_id_created ON conversations(user_id, created_at);

-- Messages table
CREATE INDEX ix_messages_conversation_id_created ON messages(conversation_id, created_at);
CREATE INDEX ix_messages_user_id_conversation_id ON messages(user_id, conversation_id);
```

**Query Performance**:
- Get conversations: O(log n) via user_id index
- Get messages: O(log n + k) where k = number of messages (via conversation_id index)
- Expected latency: < 50ms for typical conversation sizes (< 1000 messages)

**Alternatives Considered**:
- Full-text search on message content: Deferred to Phase IV (not required for Phase III)
- Table partitioning by user_id: Deferred (premature optimization for expected scale)

---

## Technology Stack Summary

**Backend**:
- FastAPI 0.104+ (async ASGI framework)
- SQLModel 0.14+ (ORM with Pydantic integration)
- OpenAI Agents SDK (official package from OpenAI)
- Official MCP SDK (Model Context Protocol implementation)
- Alembic 1.12+ (database migrations)
- Pydantic 2.x (data validation)
- pytest 7.x+ (testing framework)
- tenacity (retry logic)

**Frontend**:
- Next.js 16+ (React framework with App Router)
- React 19+ (UI library)
- OpenAI ChatKit (official chat UI components)
- Better Auth (existing authentication from Phase II)
- TypeScript 5.x (type safety)
- Tailwind CSS (styling)

**Database**:
- Neon Serverless PostgreSQL (existing from Phase II)
- Extensions: conversations and messages tables
- Indexes: Composite indexes for performance

**Deployment**:
- Docker Compose (local development and production)
- Environment variables for configuration
- Health check endpoints for monitoring

---

## Implementation Readiness

All research questions resolved. Ready to proceed to Phase 1 (Data Modeling & Contracts).

**Next Steps**:
1. Generate data-model.md with entity definitions
2. Generate API contracts in contracts/
3. Generate quickstart.md with setup instructions
4. Update agent context with new technologies
