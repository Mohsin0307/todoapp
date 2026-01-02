"""
Task Model - SQLModel Definition

Represents a task entity with user ownership and soft delete support.
"""
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import Column, Index, String, CheckConstraint
from sqlmodel import Field, SQLModel


class Task(SQLModel, table=True):
    """
    Task entity for todo items.

    Attributes:
        id: Unique task identifier (UUID)
        user_id: Owner user identifier (UUID) - indexed for efficient queries
        title: Task title (1-200 characters, required)
        description: Optional detailed description
        completed: Completion status (default: False)
        created_at: Task creation timestamp
        updated_at: Last modification timestamp
        deleted_at: Soft delete timestamp (NULL if active)
    """

    __tablename__ = "tasks"

    # Primary Key
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        nullable=False,
        description="Unique task identifier"
    )

    # Foreign Key - User ownership
    user_id: UUID = Field(
        index=True,
        nullable=False,
        description="Owner user identifier (references Better Auth user)"
    )

    # Task Content
    title: str = Field(
        sa_column=Column(
            String(200),
            nullable=False,
            # Validate title length >= 1
        ),
        min_length=1,
        max_length=200,
        description="Task title (1-200 characters)"
    )

    description: Optional[str] = Field(
        default=None,
        nullable=True,
        description="Optional detailed description"
    )

    # Status
    completed: bool = Field(
        default=False,
        nullable=False,
        description="Completion status"
    )

    # Timestamps
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Task creation timestamp"
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Last modification timestamp"
    )

    # Soft Delete
    deleted_at: Optional[datetime] = Field(
        default=None,
        nullable=True,
        description="Soft delete timestamp (NULL if active)"
    )

    __table_args__ = (
        # Composite index for efficient user task queries with ordering
        Index("ix_tasks_user_created", "user_id", "created_at"),

        # Partial index for active (non-deleted) tasks
        Index(
            "ix_tasks_active",
            "user_id",
            "deleted_at",
            postgresql_where="deleted_at IS NULL"
        ),

        # Check constraint for title length
        CheckConstraint("LENGTH(title) >= 1", name="check_title_not_empty"),
    )

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "user_id": "123e4567-e89b-12d3-a456-426614174001",
                "title": "Complete project documentation",
                "description": "Write comprehensive README and API docs",
                "completed": False,
                "created_at": "2025-12-31T10:00:00Z",
                "updated_at": "2025-12-31T10:00:00Z",
                "deleted_at": None,
            }
        }
