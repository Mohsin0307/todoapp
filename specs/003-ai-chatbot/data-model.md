# Data Model: AI-Powered Todo Chatbot (Phase III)

**Feature**: 003-ai-chatbot
**Date**: 2025-12-31
**Status**: Complete

## Overview

Phase III extends the Phase II database schema with two new tables to support conversation persistence. The existing Task and User models remain unchanged and are reused for MCP tool operations.

## Entity Relationship Diagram

```
┌─────────────┐
│    User     │  (existing from Phase II)
│─────────────│
│ id (PK)     │
│ email       │
│ name        │
│ created_at  │
└─────────────┘
      │
      │ 1:N
      ▼
┌──────────────────┐
│  Conversation    │  (NEW)
│──────────────────│
│ id (PK)          │
│ user_id (FK)     │◄──┐
│ created_at       │   │
│ updated_at       │   │
└──────────────────┘   │
      │                │
      │ 1:N            │
      ▼                │
┌──────────────────┐   │
│    Message       │  (NEW)
│──────────────────│   │
│ id (PK)          │   │
│ conversation_id  │───┘
│ user_id (FK)     │
│ role             │
│ content          │
│ created_at       │
└──────────────────┘

┌─────────────┐
│    Task     │  (existing from Phase II - no changes)
│─────────────│
│ id (PK)     │
│ user_id (FK)│
│ title       │
│ description │
│ status      │
│ created_at  │
│ completed_at│
└─────────────┘
```

## Entity Definitions

### Conversation (NEW)

**Purpose**: Represents a chat session between a user and the AI assistant. Groups related messages together for conversation history.

**SQLModel Definition**:
```python
from sqlmodel import SQLModel, Field, Relationship, Index
from datetime import datetime
from typing import Optional, List

class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    # Primary Key
    id: Optional[int] = Field(default=None, primary_key=True)

    # Foreign Keys
    user_id: str = Field(foreign_key="users.id", index=True, nullable=False)

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationships
    messages: List["Message"] = Relationship(back_populates="conversation", cascade_delete=True)

    # Table Configuration
    __table_args__ = (
        Index("ix_conversations_user_id_created", "user_id", "created_at"),
    )

    class Config:
        arbitrary_types_allowed = True
```

**Attributes**:
- `id` (int, PK): Auto-incrementing primary key
- `user_id` (str, FK → users.id): Owner of the conversation (indexed for fast user queries)
- `created_at` (datetime): When conversation started (UTC timestamp)
- `updated_at` (datetime): Last message timestamp (updated on new messages)

**Relationships**:
- `messages`: One-to-many relationship with Message table (cascade delete: deleting conversation deletes all messages)

**Indexes**:
- `ix_conversations_user_id_created`: Composite index on (user_id, created_at) for fast retrieval of user's conversations sorted by date

**Validation Rules**:
- `user_id` must reference an existing user in users table
- `created_at` and `updated_at` automatically managed by database

**Usage**:
- Created when user starts first chat (no conversation_id provided)
- Reused for subsequent messages in same conversation
- Deleted when user deletes conversation (cascades to messages)

---

### Message (NEW)

**Purpose**: Represents a single message in a conversation. Can be from user ("user" role) or AI assistant ("assistant" role).

**SQLModel Definition**:
```python
from sqlmodel import SQLModel, Field, Relationship, Index, Column, Text, Enum
from datetime import datetime
from typing import Optional
import enum

class MessageRole(str, enum.Enum):
    USER = "user"
    ASSISTANT = "assistant"

class Message(SQLModel, table=True):
    __tablename__ = "messages"

    # Primary Key
    id: Optional[int] = Field(default=None, primary_key=True)

    # Foreign Keys
    conversation_id: int = Field(foreign_key="conversations.id", index=True, nullable=False)
    user_id: str = Field(foreign_key="users.id", index=True, nullable=False)

    # Message Content
    role: str = Field(sa_column=Column(Enum(MessageRole), nullable=False))
    content: str = Field(sa_column=Column(Text, nullable=False))

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationships
    conversation: Optional[Conversation] = Relationship(back_populates="messages")

    # Table Configuration
    __table_args__ = (
        Index("ix_messages_conversation_id_created", "conversation_id", "created_at"),
        Index("ix_messages_user_id_conversation_id", "user_id", "conversation_id"),
    )

    class Config:
        arbitrary_types_allowed = True
```

**Attributes**:
- `id` (int, PK): Auto-incrementing primary key
- `conversation_id` (int, FK → conversations.id): Conversation this message belongs to (indexed)
- `user_id` (str, FK → users.id): User who owns this conversation (indexed for security scoping)
- `role` (enum): Either "user" (message from user) or "assistant" (response from AI)
- `content` (text): Message content (max 10,000 characters, enforced in application layer)
- `created_at` (datetime): When message was sent (UTC timestamp)

**Relationships**:
- `conversation`: Many-to-one relationship with Conversation table

**Indexes**:
- `ix_messages_conversation_id_created`: Composite index on (conversation_id, created_at) for fast retrieval of conversation history sorted chronologically
- `ix_messages_user_id_conversation_id`: Composite index on (user_id, conversation_id) for user-scoped queries (security)

**Validation Rules**:
- `conversation_id` must reference an existing conversation
- `user_id` must reference an existing user
- `role` must be "user" or "assistant" (enum constraint)
- `content` must not be empty (enforced in application layer)
- `content` max length 10,000 characters (enforced in application layer)

**Usage**:
- User message stored when POST /api/{user_id}/chat receives message
- Assistant message stored after AI agent generates response
- Retrieved in chronological order for conversation context (limited to last 50 messages per research.md)

---

### Task (Existing - No Changes)

**Purpose**: Represents a user's task. Managed through MCP tools invoked by AI agent.

**SQLModel Definition** (existing from Phase II):
```python
class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True, nullable=False)
    title: str = Field(max_length=200, nullable=False)
    description: Optional[str] = Field(default=None, max_length=1000)
    status: str = Field(default="pending")  # "pending" or "completed"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = Field(default=None)

    __table_args__ = (
        Index("ix_tasks_user_id_status", "user_id", "status"),
    )
```

**Integration with Phase III**:
- MCP tools (add_task, get_tasks, update_task_status, delete_task, get_task_statistics) perform CRUD operations on this table
- No schema changes needed
- Existing indexes sufficient for MCP tool queries

---

### User (Existing - No Changes)

**Purpose**: Represents a user account with authentication credentials.

**SQLModel Definition** (existing from Phase II):
```python
class User(SQLModel, table=True):
    __tablename__ = "users"

    id: str = Field(primary_key=True)  # Better Auth user ID
    email: str = Field(unique=True, index=True)
    name: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Better Auth manages password hashing
```

**Integration with Phase III**:
- `user_id` referenced in Conversation, Message, and Task tables
- JWT authentication extracts user_id from token
- No schema changes needed

---

## Database Migrations

### Migration 1: Add Conversations Table

**File**: `alembic/versions/xxx_add_conversations.py`

```python
"""Add conversations table

Revision ID: xxx
Revises: yyy  # Previous migration
Create Date: 2025-12-31
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = 'xxx'
down_revision = 'yyy'  # ID of last Phase II migration
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'conversations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_conversations_user_id', 'conversations', ['user_id'])
    op.create_index('ix_conversations_user_id_created', 'conversations', ['user_id', 'created_at'])

def downgrade():
    op.drop_index('ix_conversations_user_id_created', table_name='conversations')
    op.drop_index('ix_conversations_user_id', table_name='conversations')
    op.drop_table('conversations')
```

### Migration 2: Add Messages Table

**File**: `alembic/versions/yyy_add_messages.py`

```python
"""Add messages table

Revision ID: yyy
Revises: xxx
Create Date: 2025-12-31
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = 'yyy'
down_revision = 'xxx'  # Add conversations migration
branch_labels = None
depends_on = None

def upgrade():
    # Create enum type
    op.execute("CREATE TYPE message_role AS ENUM ('user', 'assistant')")

    op.create_table(
        'messages',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('conversation_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('role', postgresql.ENUM('user', 'assistant', name='message_role'), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_messages_conversation_id', 'messages', ['conversation_id'])
    op.create_index('ix_messages_conversation_id_created', 'messages', ['conversation_id', 'created_at'])
    op.create_index('ix_messages_user_id_conversation_id', 'messages', ['user_id', 'conversation_id'])

def downgrade():
    op.drop_index('ix_messages_user_id_conversation_id', table_name='messages')
    op.drop_index('ix_messages_conversation_id_created', table_name='messages')
    op.drop_index('ix_messages_conversation_id', table_name='messages')
    op.drop_table('messages')
    op.execute("DROP TYPE message_role")
```

---

## Query Patterns

### Get User's Conversations (Most Recent First)

```python
conversations = db.query(Conversation).filter(
    Conversation.user_id == user_id
).order_by(Conversation.updated_at.desc()).limit(20).all()
```

**Performance**: O(log n) via ix_conversations_user_id_created index

### Get Conversation History (Last 50 Messages)

```python
messages = db.query(Message).filter(
    Message.conversation_id == conversation_id,
    Message.user_id == user_id  # Security: ensure user owns conversation
).order_by(Message.created_at.desc()).limit(50).all()

# Reverse to chronological order
messages = list(reversed(messages))
```

**Performance**: O(log n + 50) via ix_messages_conversation_id_created index

### Create New Message

```python
message = Message(
    conversation_id=conversation_id,
    user_id=user_id,
    role="user",
    content=user_input
)
db.add(message)
db.commit()
```

**Performance**: O(log n) for index updates

---

## Data Integrity

### Foreign Key Constraints

- `conversations.user_id` → `users.id` (CASCADE on delete)
- `messages.conversation_id` → `conversations.id` (CASCADE on delete)
- `messages.user_id` → `users.id` (CASCADE on delete)

**Behavior**:
- Deleting a user deletes all their conversations and messages
- Deleting a conversation deletes all its messages
- Database enforces referential integrity

### Application-Level Validation

- Message content max length: 10,000 characters
- Message role must be "user" or "assistant"
- User message trimmed of leading/trailing whitespace
- Empty messages rejected

---

## Storage Estimates

**Assumptions**:
- Average conversation: 20 messages
- Average message: 100 characters
- 1000 users, 5 conversations each, 20 messages per conversation

**Storage**:
- Conversations: 5,000 rows × 50 bytes = 250 KB
- Messages: 100,000 rows × 200 bytes = 20 MB
- Total: ~20 MB for base data + indexes

**Scale**: Neon PostgreSQL easily handles this volume. No partitioning needed for Phase III scale.

---

## Implementation Checklist

- [ ] Create Conversation SQLModel in backend/models/conversation.py
- [ ] Create Message SQLModel in backend/models/message.py
- [ ] Update backend/models/__init__.py to export new models
- [ ] Generate Alembic migration for conversations table
- [ ] Generate Alembic migration for messages table
- [ ] Run migrations locally and verify schema
- [ ] Test conversation creation and message insertion
- [ ] Test cascade deletes (conversation → messages)
- [ ] Verify indexes created correctly
- [ ] Test query performance with sample data
