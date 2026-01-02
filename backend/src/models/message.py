"""Message model for conversation messages."""
from sqlmodel import SQLModel, Field, Relationship, Index, Column, Text, Enum as SQLEnum
from datetime import datetime
from typing import Optional
import enum

class MessageRole(str, enum.Enum):
    """Role of message sender."""
    USER = "user"
    ASSISTANT = "assistant"

class Message(SQLModel, table=True):
    """
    Represents a single message in a conversation.

    Can be from user ("user" role) or AI assistant ("assistant" role).
    """
    __tablename__ = "messages"

    # Primary Key
    id: Optional[int] = Field(default=None, primary_key=True)

    # Foreign Keys
    conversation_id: int = Field(foreign_key="conversations.id", index=True, nullable=False)
    user_id: str = Field(foreign_key="users.id", index=True, nullable=False)

    # Message Content
    role: MessageRole = Field(sa_column=Column(SQLEnum(MessageRole), nullable=False))
    content: str = Field(sa_column=Column(Text, nullable=False))

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationships
    conversation: Optional["Conversation"] = Relationship(back_populates="messages")

    # Table Configuration
    __table_args__ = (
        Index("ix_messages_conversation_id_created", "conversation_id", "created_at"),
        Index("ix_messages_user_id_conversation_id", "user_id", "conversation_id"),
    )

    class Config:
        arbitrary_types_allowed = True
