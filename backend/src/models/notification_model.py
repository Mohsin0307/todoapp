"""
Notification Model - Reminders and system alerts.

Stores notifications for users triggered by events or schedules.
"""
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import Column, Index, String, Text
from sqlmodel import Field, SQLModel


class Notification(SQLModel, table=True):
    """Notification entity for reminders and alerts."""

    __tablename__ = "notifications"

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True, nullable=False)
    user_id: UUID = Field(index=True, nullable=False)
    type: str = Field(sa_column=Column(String(20), nullable=False))
    title: str = Field(sa_column=Column(String(255), nullable=False))
    message: str = Field(sa_column=Column(Text, nullable=False))
    priority: str = Field(
        default="normal",
        sa_column=Column(String(10), nullable=False),
    )

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    scheduled_for: Optional[datetime] = Field(default=None)
    sent_at: Optional[datetime] = Field(default=None)
    read_at: Optional[datetime] = Field(default=None)

    # Status flags
    is_read: bool = Field(default=False)
    is_delivered: bool = Field(default=False)
    delivery_method: str = Field(
        default="in_app",
        sa_column=Column(String(20), nullable=False),
    )

    # Associations
    todo_id: Optional[UUID] = Field(default=None, foreign_key="todo_items.id")
    event_id: Optional[str] = Field(default=None, sa_column=Column(String(36), nullable=True))

    __table_args__ = (
        Index("ix_notifications_user_read", "user_id", "is_read"),
        Index("ix_notifications_scheduled", "scheduled_for"),
    )
