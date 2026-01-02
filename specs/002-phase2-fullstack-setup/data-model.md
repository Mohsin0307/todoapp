# Data Model: Phase II Full-Stack Web Application

**Date**: 2025-12-30
**Purpose**: Define database schema, entities, relationships, and validation rules

---

## Entity: User

**Managed By**: Better Auth (do not create or modify manually)

**Table Name**: `users`

**Description**: User accounts managed entirely by Better Auth library. Application code should treat this table as read-only.

**Key Fields** (reference only):
- `id` (UUID, primary key) - Unique user identifier
- `email` (VARCHAR(255), unique, NOT NULL) - User email address
- `password_hash` (VARCHAR(255), NOT NULL) - Bcrypt hashed password
- `created_at` (TIMESTAMP, default NOW()) - Account creation time
- `updated_at` (TIMESTAMP, default NOW()) - Last profile update

**Relationships**:
- One-to-Many with Task (user → many tasks)

**Notes**:
- Better Auth handles all user CRUD operations
- Password hashing, email verification, session management automated
- Do NOT create custom user fields in this table - use separate profile table if needed
- Foreign keys from other tables CAN reference `users.id`

---

## Entity: Task

**Managed By**: Application (custom implementation)

**Table Name**: `tasks`

**Description**: User-created todo tasks with title, description, and completion status. Each task belongs to exactly one user and supports soft deletion.

### Fields

| Field | Type | Constraints | Default | Description |
|-------|------|-------------|---------|-------------|
| `id` | UUID | PRIMARY KEY | `gen_random_uuid()` | Unique task identifier |
| `user_id` | UUID | FOREIGN KEY → users.id, NOT NULL, INDEXED | - | Owner user ID (ensures task ownership) |
| `title` | VARCHAR(200) | NOT NULL, CHECK(length >= 1) | - | Task title (required, non-empty) |
| `description` | TEXT | NULLABLE | NULL | Optional detailed description |
| `completed` | BOOLEAN | NOT NULL | FALSE | Completion status (false = pending, true = done) |
| `created_at` | TIMESTAMP | NOT NULL | NOW() | Task creation timestamp (auto-generated) |
| `updated_at` | TIMESTAMP | NOT NULL | NOW() | Last modification timestamp (auto-updated) |
| `deleted_at` | TIMESTAMP | NULLABLE | NULL | Soft delete timestamp (NULL = active, timestamp = deleted) |

### Relationships

- **User** (Many-to-One):
  - Foreign Key: `tasks.user_id` → `users.id`
  - Cascade: ON DELETE CASCADE (if user deleted, all their tasks deleted)
  - Lazy Loading: User object not loaded by default (avoid N+1 queries)

### Indexes

1. **Primary Index**: `id` (automatic, unique)
2. **Foreign Key Index**: `user_id` (for efficient user-scoped queries)
3. **Composite Index**: `(user_id, created_at DESC)` (for paginated task lists ordered by creation date)
4. **Soft Delete Index**: `deleted_at` WHERE `deleted_at IS NOT NULL` (partial index for trash/archive views)

**Index Justification**:
- `user_id` index: Every query filters by user (enforces data isolation)
- Composite `(user_id, created_at)`: Optimizes common pattern: "get user's tasks ordered by date"
- Soft delete partial index: Only indexes deleted tasks (smaller index, faster queries)

### Validation Rules

**Application-Level Validation** (Pydantic/SQLModel):
1. **Title**:
   - MUST NOT be empty string
   - MUST be 1-200 characters
   - Leading/trailing whitespace SHOULD be trimmed before save
   - Example invalid: `""`, `"   "` (only whitespace)
   - Example valid: `"Buy groceries"`, `"A" * 200`

2. **Description**:
   - OPTIONAL (can be NULL or empty string)
   - No length limit (TEXT type)
   - Sanitize HTML if rendering (prevent XSS)

3. **User ID**:
   - MUST reference existing user in `users` table (enforced by FK constraint)
   - MUST match authenticated user's ID (enforced in business logic)
   - Example: Reject if `task.user_id != jwt_user_id`

4. **Completed**:
   - MUST be boolean (true/false)
   - Defaults to `false` on creation
   - Can be toggled multiple times (no state restrictions)

**Database-Level Constraints**:
- `CHECK (length(title) >= 1)` - Ensures non-empty title
- `FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE` - Referential integrity
- `NOT NULL` constraints on `id`, `user_id`, `title`, `completed`, `created_at`, `updated_at`

### State Transitions

**Completion States**:
```
[Created] → completed = FALSE (default)
    ↓
[Toggle] → completed = TRUE
    ↓
[Toggle] → completed = FALSE (can toggle back)
```

**Lifecycle States**:
```
[Active] → deleted_at = NULL (visible to user)
    ↓
[Soft Delete] → deleted_at = NOW() (hidden, can be restored)
    ↓
[Hard Delete] → Row permanently removed (optional cleanup job)
```

**Allowed Transitions**:
1. **Create**: New task with `completed = FALSE`, `deleted_at = NULL`
2. **Complete**: Set `completed = TRUE`, update `updated_at`
3. **Uncomplete**: Set `completed = FALSE`, update `updated_at`
4. **Edit**: Modify `title` or `description`, update `updated_at`
5. **Soft Delete**: Set `deleted_at = NOW()`, keep in database
6. **Restore** (optional): Set `deleted_at = NULL`, update `updated_at`
7. **Hard Delete** (optional): DELETE FROM tasks WHERE id = ?

**Business Rules**:
- Cannot modify task belonging to different user (enforced by checking `user_id == jwt_user_id`)
- Cannot restore task deleted by another user
- Soft-deleted tasks excluded from normal queries (WHERE deleted_at IS NULL)
- All state changes update `updated_at` timestamp

---

## SQLModel Implementation

**File**: `backend/src/models/task.py`

```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional

class TaskBase(SQLModel):
    """Base fields for Task (shared between DB model and API schemas)"""
    title: str = Field(max_length=200, min_length=1, description="Task title")
    description: Optional[str] = Field(default=None, description="Optional task description")
    completed: bool = Field(default=False, description="Completion status")


class Task(TaskBase, table=True):
    """Database model for tasks table"""
    __tablename__ = "tasks"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", nullable=False, index=True)

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    deleted_at: Optional[datetime] = Field(default=None)

    # Relationships (lazy-loaded)
    # user: Optional["User"] = Relationship(back_populates="tasks")


class TaskCreate(TaskBase):
    """API schema for creating tasks (excludes id, user_id, timestamps)"""
    pass


class TaskUpdate(SQLModel):
    """API schema for updating tasks (all fields optional)"""
    title: Optional[str] = Field(default=None, max_length=200, min_length=1)
    description: Optional[str] = None
    completed: Optional[bool] = None


class TaskRead(TaskBase):
    """API schema for reading tasks (includes all fields)"""
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Enable ORM mode for SQLModel compatibility
```

**Usage Examples**:

```python
# Create new task
async def create_task(task_data: TaskCreate, user_id: UUID, session: AsyncSession):
    task = Task(
        **task_data.dict(),
        user_id=user_id  # From JWT token
    )
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task

# Get user's tasks (user-scoped query)
async def get_user_tasks(user_id: UUID, session: AsyncSession):
    result = await session.execute(
        select(Task)
        .where(Task.user_id == user_id)
        .where(Task.deleted_at.is_(None))  # Exclude soft-deleted
        .order_by(Task.created_at.desc())
    )
    return result.scalars().all()

# Soft delete task
async def soft_delete_task(task_id: UUID, user_id: UUID, session: AsyncSession):
    task = await session.get(Task, task_id)
    if not task or task.deleted_at is not None:
        raise NotFoundError("Task not found")
    if task.user_id != user_id:
        raise PermissionError("Not authorized to delete this task")

    task.deleted_at = datetime.utcnow()
    task.updated_at = datetime.utcnow()
    await session.commit()

# Toggle completion
async def toggle_completion(task_id: UUID, user_id: UUID, session: AsyncSession):
    task = await session.get(Task, task_id)
    if not task or task.deleted_at is not None:
        raise NotFoundError("Task not found")
    if task.user_id != user_id:
        raise PermissionError("Not authorized to modify this task")

    task.completed = not task.completed
    task.updated_at = datetime.utcnow()
    await session.commit()
    await session.refresh(task)
    return task
```

---

## Alembic Migration Example

**File**: `backend/alembic/versions/001_create_tasks_table.py`

```python
"""Create tasks table

Revision ID: 001
Revises:
Create Date: 2025-12-30
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'tasks',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('completed', sa.Boolean(), nullable=False, server_default=sa.text('FALSE')),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.CheckConstraint('LENGTH(title) >= 1', name='title_not_empty')
    )

    # Composite index for user-scoped queries
    op.create_index('idx_tasks_user_created', 'tasks', ['user_id', sa.text('created_at DESC')])

    # Partial index for soft-deleted tasks
    op.execute('CREATE INDEX idx_tasks_deleted ON tasks(deleted_at) WHERE deleted_at IS NOT NULL')


def downgrade():
    op.drop_index('idx_tasks_deleted', table_name='tasks')
    op.drop_index('idx_tasks_user_created', table_name='tasks')
    op.drop_table('tasks')
```

---

## Summary

**Entities**: 2 (User - managed by Better Auth, Task - custom)

**Relationships**: 1 (User → Task, one-to-many, cascading delete)

**Key Design Decisions**:
1. **Soft Deletes**: Preserve audit trail, allow task restoration
2. **User-Scoped Queries**: Every query filters by `user_id` for data isolation
3. **Composite Index**: Optimizes common pattern (user's tasks ordered by date)
4. **Validation**: Both database constraints (CHECK) and application logic (Pydantic)
5. **SQLModel**: Single model serves as DB table, Pydantic schema, and API type

**Security**:
- User ID enforced from JWT token, not request body (prevents privilege escalation)
- Foreign key constraint ensures referential integrity
- Soft deletes prevent accidental data loss

**Performance**:
- Indexed `user_id` and `(user_id, created_at)` for fast queries
- Partial index on `deleted_at` reduces index size
- Lazy-loaded relationships avoid N+1 queries

**Compliance**:
- ✅ Constitution Principle VI (Code Quality): Type-safe models, validation rules
- ✅ Constitution Principle VII (Security): User isolation enforced, no manual user_id injection
- ✅ Constitution Principle IX (Performance): Indexed queries, efficient soft deletes
