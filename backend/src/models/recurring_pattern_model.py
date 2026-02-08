"""
RecurringPattern Model - Reusable recurring task patterns.
"""
from datetime import datetime, time
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import Column, String
from sqlmodel import Field, SQLModel


class RecurringPattern(SQLModel, table=True):
    """Defines recurring task patterns that can be reused."""

    __tablename__ = "recurring_patterns"

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True, nullable=False)
    name: str = Field(sa_column=Column(String(100), unique=True, nullable=False))
    pattern_type: str = Field(sa_column=Column(String(20), nullable=False))
    interval: int = Field(default=1)
    day_of_week: Optional[int] = Field(default=None, ge=0, le=6)
    day_of_month: Optional[int] = Field(default=None, ge=1, le=31)
    month: Optional[int] = Field(default=None, ge=1, le=12)
    time_of_day: Optional[str] = Field(default="09:00", sa_column=Column(String(10), nullable=True))
    created_by: UUID = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    is_active: bool = Field(default=True)
