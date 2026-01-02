# Phase III: AI-Powered Todo Chatbot - Overview

## Transformation
From: Web UI with forms and buttons
To: Chat interface with natural language

## User Experience

### Before (Phase II):
```
[Form]
Title: ___________
Description: ___________
[Create Task Button]
```

### After (Phase III):
```
User: Add a task to buy groceries
AI: ✅ Added task: Buy groceries

User: What's pending?
AI: You have 2 pending tasks:
    1. Buy groceries
    2. Call mom
```

## Architecture Components

### 1. ChatKit Frontend
- OpenAI's official chat UI
- Message history
- Typing indicators
- Streaming responses

### 2. Chat Endpoint (FastAPI)
- POST /api/{user_id}/chat
- Receives user message
- Returns AI response
- Manages conversation state in DB

### 3. OpenAI Agents SDK
- Runs AI agent
- Decides which tools to use
- Chains multiple tools if needed
- Generates natural language responses

### 4. MCP Server
- 5 stateless tools
- Task CRUD operations
- User-scoped data access
- PostgreSQL backend

### 5. Database Schema
- Conversations table (user_id, created_at)
- Messages table (conversation_id, role, content, timestamp)
- Tasks table (existing from Phase II)

## Request Flow

```
┌─────────────────────────────────────────────┐
│ 1. User types message in chat UI          │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│ 2. Frontend POST /api/{user_id}/chat      │
│    Body: { "message": "Add task..." }      │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│ 3. Backend authenticates user via JWT     │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│ 4. Load conversation history from DB      │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│ 5. Pass to OpenAI Agents SDK with:        │
│    - User message                           │
│    - Conversation history                   │
│    - Available MCP tools                    │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│ 6. Agent decides which tool(s) to call    │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│ 7. MCP server executes tool(s)            │
│    - Query/update PostgreSQL               │
│    - Return results to agent               │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│ 8. Agent generates natural language reply │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│ 9. Backend saves messages to DB           │
│    - User message                           │
│    - AI response                            │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│ 10. User sees message in chat UI          │
└─────────────────────────────────────────────┘
```

## Key Benefits

### Stateless Architecture
- Server holds NO state
- Can restart anytime
- Horizontally scalable
- Load balancer friendly

### MCP Standards
- Reusable tools
- Well-defined interfaces
- Easy to extend
- Compatible with other AI systems

### Natural Language
- Intuitive user experience
- No learning curve
- Conversational
- Context-aware

## Success Metrics
- [ ] User can manage all tasks via chat
- [ ] Agent understands various phrasings
- [ ] Conversation persists across sessions
- [ ] Server can restart without losing state
- [ ] Response time < 2 seconds
- [ ] Tool calls are accurate
