# MCP Tools Specification

## Overview
5 MCP tools for task management operations.
All tools are stateless and store data in PostgreSQL.

## Design Principles
1. **Stateless**: No in-memory state
2. **User-scoped**: All operations filtered by user_id
3. **Database-backed**: All data persists
4. **Error handling**: Graceful failure modes
5. **Return structure**: Consistent response format

## Tool 1: add_task

**Purpose:** Create a new task for the user

**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "user_id": {"type": "string", "description": "User identifier"},
    "title": {"type": "string", "description": "Task title", "maxLength": 200},
    "description": {"type": "string", "description": "Optional task description", "maxLength": 1000}
  },
  "required": ["user_id", "title"]
}
```

**Output Schema:**
```json
{
  "task_id": "integer",
  "status": "string (created)",
  "title": "string",
  "description": "string or null",
  "created_at": "ISO 8601 timestamp"
}
```

**Example Usage:**
```json
// Input
{
  "user_id": "user_123",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}

// Output
{
  "task_id": 42,
  "status": "created",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "created_at": "2025-12-31T10:30:00Z"
}
```

**Error Cases:**
- `title` empty or whitespace-only → `{"error": "Title cannot be empty"}`
- `title` > 200 chars → `{"error": "Title exceeds 200 character limit"}`
- `description` > 1000 chars → `{"error": "Description exceeds 1000 character limit"}`
- Database connection failure → `{"error": "Unable to save task. Please try again."}`

---

## Tool 2: get_tasks

**Purpose:** Retrieve all tasks for the user with optional filtering

**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "user_id": {"type": "string", "description": "User identifier"},
    "status": {"type": "string", "enum": ["pending", "completed", "all"], "description": "Filter by status", "default": "all"}
  },
  "required": ["user_id"]
}
```

**Output Schema:**
```json
{
  "tasks": [
    {
      "task_id": "integer",
      "title": "string",
      "description": "string or null",
      "status": "string (pending|completed)",
      "created_at": "ISO 8601 timestamp",
      "completed_at": "ISO 8601 timestamp or null"
    }
  ],
  "count": "integer"
}
```

**Example Usage:**
```json
// Input
{
  "user_id": "user_123",
  "status": "pending"
}

// Output
{
  "tasks": [
    {
      "task_id": 42,
      "title": "Buy groceries",
      "description": "Milk, eggs, bread",
      "status": "pending",
      "created_at": "2025-12-31T10:30:00Z",
      "completed_at": null
    },
    {
      "task_id": 43,
      "title": "Call mom",
      "description": null,
      "status": "pending",
      "created_at": "2025-12-31T11:00:00Z",
      "completed_at": null
    }
  ],
  "count": 2
}
```

**Error Cases:**
- Invalid `status` value → `{"error": "Status must be 'pending', 'completed', or 'all'"}`
- Database connection failure → `{"error": "Unable to retrieve tasks. Please try again."}`

---

## Tool 3: update_task_status

**Purpose:** Mark a task as completed or revert to pending

**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "user_id": {"type": "string", "description": "User identifier"},
    "task_id": {"type": "integer", "description": "Task ID to update"},
    "status": {"type": "string", "enum": ["pending", "completed"], "description": "New status"}
  },
  "required": ["user_id", "task_id", "status"]
}
```

**Output Schema:**
```json
{
  "task_id": "integer",
  "title": "string",
  "status": "string (pending|completed)",
  "completed_at": "ISO 8601 timestamp or null"
}
```

**Example Usage:**
```json
// Input
{
  "user_id": "user_123",
  "task_id": 42,
  "status": "completed"
}

// Output
{
  "task_id": 42,
  "title": "Buy groceries",
  "status": "completed",
  "completed_at": "2025-12-31T14:30:00Z"
}
```

**Error Cases:**
- `task_id` not found → `{"error": "Task not found"}`
- Task belongs to different user → `{"error": "Task not found"}` (security: don't reveal existence)
- Invalid `status` value → `{"error": "Status must be 'pending' or 'completed'"}`
- Database connection failure → `{"error": "Unable to update task. Please try again."}`

---

## Tool 4: delete_task

**Purpose:** Permanently delete a task

**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "user_id": {"type": "string", "description": "User identifier"},
    "task_id": {"type": "integer", "description": "Task ID to delete"}
  },
  "required": ["user_id", "task_id"]
}
```

**Output Schema:**
```json
{
  "task_id": "integer",
  "title": "string",
  "deleted": "boolean (true)",
  "deleted_at": "ISO 8601 timestamp"
}
```

**Example Usage:**
```json
// Input
{
  "user_id": "user_123",
  "task_id": 42
}

// Output
{
  "task_id": 42,
  "title": "Buy groceries",
  "deleted": true,
  "deleted_at": "2025-12-31T15:00:00Z"
}
```

**Error Cases:**
- `task_id` not found → `{"error": "Task not found"}`
- Task belongs to different user → `{"error": "Task not found"}` (security: don't reveal existence)
- Database connection failure → `{"error": "Unable to delete task. Please try again."}`

---

## Tool 5: get_task_statistics

**Purpose:** Get analytics and summary statistics for user's tasks

**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "user_id": {"type": "string", "description": "User identifier"}
  },
  "required": ["user_id"]
}
```

**Output Schema:**
```json
{
  "total_tasks": "integer",
  "pending_tasks": "integer",
  "completed_tasks": "integer",
  "completion_rate": "float (0.0 to 1.0)",
  "tasks_created_today": "integer",
  "tasks_completed_today": "integer"
}
```

**Example Usage:**
```json
// Input
{
  "user_id": "user_123"
}

// Output
{
  "total_tasks": 10,
  "pending_tasks": 3,
  "completed_tasks": 7,
  "completion_rate": 0.7,
  "tasks_created_today": 2,
  "tasks_completed_today": 1
}
```

**Error Cases:**
- Database connection failure → `{"error": "Unable to retrieve statistics. Please try again."}`

---

## Implementation Guidelines

### Database Queries
- All queries MUST include `WHERE user_id = ?` filter
- Use parameterized queries to prevent SQL injection
- Handle NULL values gracefully in optional fields
- Use database timestamps (server-side) for consistency

### Error Handling
- Return user-friendly error messages (no stack traces)
- Log detailed errors server-side for debugging
- Use appropriate HTTP status codes when exposed via API
- Never expose user_id mismatches (security)

### Performance
- Index `user_id` column for fast filtering
- Index `status` column for filtered queries
- Consider pagination for `get_tasks` if user has many tasks
- Cache user statistics with short TTL (optional optimization)

### Security
- Validate all inputs against schema
- Sanitize string inputs
- Enforce user_id scope strictly (never cross-user access)
- Rate limit tool calls per user (prevent abuse)

### Testing
- Unit test each tool in isolation
- Test with valid inputs
- Test all error cases
- Test user_id scoping (ensure data isolation)
- Test concurrent operations (multiple users)
- Test database failure recovery

---

## Natural Language Examples

### Creating Tasks
```
User: "Add a task to buy groceries"
→ Tool: add_task(user_id="user_123", title="Buy groceries")

User: "Remind me to call mom tomorrow"
→ Tool: add_task(user_id="user_123", title="Call mom tomorrow")

User: "Create a task: finish the report. Include details: quarterly sales analysis"
→ Tool: add_task(user_id="user_123", title="Finish the report", description="Quarterly sales analysis")
```

### Retrieving Tasks
```
User: "What's on my list?"
→ Tool: get_tasks(user_id="user_123", status="all")

User: "Show me pending tasks"
→ Tool: get_tasks(user_id="user_123", status="pending")

User: "What have I completed?"
→ Tool: get_tasks(user_id="user_123", status="completed")
```

### Updating Tasks
```
User: "Mark task 42 as done"
→ Tool: update_task_status(user_id="user_123", task_id=42, status="completed")

User: "I finished buying groceries"
→ Tool: get_tasks(user_id="user_123", status="pending")
→ (Agent finds task_id 42: "Buy groceries")
→ Tool: update_task_status(user_id="user_123", task_id=42, status="completed")

User: "Uncomplete task 43"
→ Tool: update_task_status(user_id="user_123", task_id=43, status="pending")
```

### Deleting Tasks
```
User: "Delete task 42"
→ Tool: delete_task(user_id="user_123", task_id=42)

User: "Remove the grocery task"
→ Tool: get_tasks(user_id="user_123", status="all")
→ (Agent finds task_id 42: "Buy groceries")
→ Tool: delete_task(user_id="user_123", task_id=42)
```

### Statistics
```
User: "How am I doing?"
→ Tool: get_task_statistics(user_id="user_123")
→ Agent response: "You have 3 pending tasks and 7 completed. That's a 70% completion rate! 🎉"

User: "What's my progress?"
→ Tool: get_task_statistics(user_id="user_123")
```

---

## Tool Registration (MCP Protocol)

Each tool must be registered with the MCP server using this format:

```python
{
  "name": "add_task",
  "description": "Create a new task for the user",
  "inputSchema": { /* JSON schema above */ }
}
```

The OpenAI Agents SDK will discover these tools and make them available to the agent automatically.
