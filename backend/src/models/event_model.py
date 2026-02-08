"""
Event Model - Event-driven architecture event tracking.

Stores events published to Kafka/Redpanda for auditing and replay.
"""
from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlalchemy import Column, Index, String, Text
from sqlmodel import Field, SQLModel


class Event(SQLModel, table=True):
    """Event entity for event-driven architecture tracking."""

    __tablename__ = "events"

    id: str = Field(
        default_factory=lambda: str(uuid4()),
        sa_column=Column(String(36), primary_key=True),
    )
    type: str = Field(sa_column=Column(String(100), nullable=False, index=True))
    source: str = Field(sa_column=Column(String(100), nullable=False))
    timestamp: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    correlation_id: Optional[str] = Field(
        default_factory=lambda: str(uuid4()),
        sa_column=Column(String(36), nullable=True),
    )
    causation_id: Optional[str] = Field(
        default=None,
        sa_column=Column(String(36), nullable=True),
    )
    payload: Optional[str] = Field(
        default=None,
        sa_column=Column(Text, nullable=True),
        description="JSON-serialized event payload",
    )
    user_id: Optional[str] = Field(default=None, sa_column=Column(String(36), nullable=True))
    todo_id: Optional[str] = Field(default=None, sa_column=Column(String(36), nullable=True))
    processed: bool = Field(default=False)
    retries: int = Field(default=0)
    max_retries: int = Field(default=3)

    __table_args__ = (
        Index("ix_events_timestamp", "timestamp"),
        Index("ix_events_processed", "processed"),
        Index("ix_events_correlation", "correlation_id"),
    )
