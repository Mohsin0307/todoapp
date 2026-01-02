"""Conversation model for AI chat sessions."""
from sqlmodel import SQLModel, Field, Relationship, Index
from datetime import datetime
from typing import Optional, List

class Conversation(SQLModel, table=True):
    """
    Represents a chat session between a user and the AI assistant.

    Groups related messages together for conversation history.
    All conversation state is persisted to support stateless architecture.
    """
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
