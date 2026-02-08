"""
TodoItem Model - Advanced Todo with recurrence, reminders, tags, priorities.

Extends the basic Task model with cloud-native features.
"""
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import Column, Index, String, Text, CheckConstraint
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlmodel import Field, SQLModel


class TodoItem(SQLModel, table=True):
    """Advanced todo item with recurrence, reminders, tags, and priorities."""

    __tablename__ = "todo_items"

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True, nullable=False)
    user_id: UUID = Field(index=True, nullable=False)

    # Core fields
    title: str = Field(
        sa_column=Column(String(255), nullable=False),
        min_length=1,
        max_length=255,
    )
    description: Optional[str] = Field(
        default=None,
        sa_column=Column(Text, nullable=True),
    )
    status: str = Field(
        default="pending",
        sa_column=Column(String(20), nullable=False),
    )
    priority: str = Field(
        default="medium",
        sa_column=Column(String(10), nullable=False),
    )
    due_date: Optional[datetime] = Field(default=None)

    # Tags stored as JSON array
    tags: Optional[str] = Field(
        default=None,
        sa_column=Column(Text, nullable=True),
        description="JSON-serialized list of tags",
    )

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Recurrence
    is_recurring: bool = Field(default=False)
    recurrence_pattern: Optional[str] = Field(
        default=None,
        sa_column=Column(String(20), nullable=True),
    )
    recurrence_interval: Optional[int] = Field(default=None)
    recurrence_end_date: Optional[datetime] = Field(default=None)

    # Reminders
    reminder_enabled: bool = Field(default=False)
    reminder_time: Optional[datetime] = Field(default=None)
    reminder_offset_hours: Optional[int] = Field(default=None)

    # Hierarchy
    parent_id: Optional[UUID] = Field(default=None, foreign_key="todo_items.id")

    __table_args__ = (
        Index("ix_todo_items_user_status", "user_id", "status"),
        Index("ix_todo_items_user_due", "user_id", "due_date"),
        Index("ix_todo_items_user_priority", "user_id", "priority"),
        CheckConstraint(
            "status IN ('pending', 'in_progress', 'completed', 'cancelled')",
            name="check_todo_status",
        ),
        CheckConstraint(
            "priority IN ('low', 'medium', 'high', 'urgent')",
            name="check_todo_priority",
        ),
    )
