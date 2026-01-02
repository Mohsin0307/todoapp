"""
Conversation Service - Business Logic for Conversation and Message Management

Provides CRUD operations for conversations and messages with user-scoped access.
Implements conversation history windowing for AI context management.
"""
from datetime import datetime
from typing import List, Optional, Dict, Any

from fastapi import HTTPException, status
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import and_

from src.models.conversation import Conversation
from src.models.message import Message, MessageRole


class ConversationService:
    """Service for conversation and message CRUD operations."""

    # Maximum messages to load for AI context (from research.md)
    MAX_CONVERSATION_HISTORY = 50

    @staticmethod
    async def create_conversation(
        session: AsyncSession,
        user_id: str
    ) -> Conversation:
        """
        Create a new conversation for the user.

        Args:
            session: Database session
            user_id: Owner user identifier

        Returns:
            Conversation: Newly created conversation

        Example:
            conversation = await ConversationService.create_conversation(session, user_id)
        """
        conversation = Conversation(
            user_id=user_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        session.add(conversation)
        await session.flush()
        await session.refresh(conversation)

        return conversation

    @staticmethod
    async def get_conversation(
        session: AsyncSession,
        conversation_id: int,
        user_id: str
    ) -> Conversation:
        """
        Get a conversation by ID (user-scoped).

        Args:
            session: Database session
            conversation_id: Conversation identifier
            user_id: Owner user identifier (for authorization)

        Returns:
            Conversation: The requested conversation

        Raises:
            HTTPException: 404 if conversation not found or doesn't belong to user

        Example:
            conversation = await ConversationService.get_conversation(session, conv_id, user_id)
        """
        query = select(Conversation).where(
            and_(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id
            )
        )

        result = await session.execute(query)
        conversation = result.scalar_one_or_none()

        if conversation is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Conversation {conversation_id} not found"
            )

        return conversation

    @staticmethod
    async def list_conversations(
        session: AsyncSession,
        user_id: str,
        limit: int = 20
    ) -> List[Conversation]:
        """
        List user's conversations (most recent first).

        Args:
            session: Database session
            user_id: Owner user identifier
            limit: Maximum number of conversations to return

        Returns:
            List[Conversation]: User's conversations

        Example:
            conversations = await ConversationService.list_conversations(session, user_id)
        """
        query = select(Conversation).where(
            Conversation.user_id == user_id
        ).order_by(desc(Conversation.updated_at)).limit(limit)

        result = await session.execute(query)
        conversations = result.scalars().all()

        return list(conversations)

    @staticmethod
    async def add_message(
        session: AsyncSession,
        conversation_id: int,
        user_id: str,
        role: MessageRole,
        content: str
    ) -> Message:
        """
        Add a message to a conversation.

        Args:
            session: Database session
            conversation_id: Conversation identifier
            user_id: Owner user identifier
            role: Message role (user or assistant)
            content: Message content

        Returns:
            Message: Newly created message

        Raises:
            HTTPException: 404 if conversation not found

        Example:
            message = await ConversationService.add_message(
                session, conv_id, user_id, MessageRole.USER, "Hello"
            )
        """
        # Verify conversation exists and belongs to user
        conversation = await ConversationService.get_conversation(
            session, conversation_id, user_id
        )

        # Create message
        message = Message(
            conversation_id=conversation_id,
            user_id=user_id,
            role=role,
            content=content,
            created_at=datetime.utcnow()
        )

        session.add(message)

        # Update conversation's updated_at timestamp
        conversation.updated_at = datetime.utcnow()

        await session.flush()
        await session.refresh(message)

        return message

    @staticmethod
    async def get_conversation_history(
        session: AsyncSession,
        conversation_id: int,
        user_id: str,
        limit: Optional[int] = None
    ) -> List[Message]:
        """
        Get conversation message history (chronological order).

        Implements windowing strategy: returns last N messages to fit AI context window.
        Default limit from research.md: 50 messages.

        Args:
            session: Database session
            conversation_id: Conversation identifier
            user_id: Owner user identifier
            limit: Maximum messages to return (default: MAX_CONVERSATION_HISTORY)

        Returns:
            List[Message]: Messages in chronological order (oldest to newest)

        Example:
            messages = await ConversationService.get_conversation_history(
                session, conv_id, user_id
            )
        """
        # Verify conversation exists and belongs to user
        await ConversationService.get_conversation(session, conversation_id, user_id)

        # Apply default limit if not specified
        if limit is None:
            limit = ConversationService.MAX_CONVERSATION_HISTORY

        # Get last N messages (most recent first)
        query = select(Message).where(
            and_(
                Message.conversation_id == conversation_id,
                Message.user_id == user_id
            )
        ).order_by(desc(Message.created_at)).limit(limit)

        result = await session.execute(query)
        messages = result.scalars().all()

        # Reverse to chronological order (oldest to newest)
        return list(reversed(messages))

    @staticmethod
    async def delete_conversation(
        session: AsyncSession,
        conversation_id: int,
        user_id: str
    ) -> None:
        """
        Delete a conversation and all its messages (cascade).

        Args:
            session: Database session
            conversation_id: Conversation identifier
            user_id: Owner user identifier

        Raises:
            HTTPException: 404 if conversation not found

        Example:
            await ConversationService.delete_conversation(session, conv_id, user_id)
        """
        conversation = await ConversationService.get_conversation(
            session, conversation_id, user_id
        )

        await session.delete(conversation)
        await session.flush()

    @staticmethod
    def messages_to_claude_format(messages: List[Message]) -> List[Dict[str, str]]:
        """
        Convert database messages to Claude API format.

        Args:
            messages: List of Message objects

        Returns:
            List of message dicts in Claude format: [{"role": "user", "content": "..."}]

        Example:
            claude_messages = ConversationService.messages_to_claude_format(messages)
        """
        return [
            {
                "role": msg.role.value if hasattr(msg.role, 'value') else msg.role,
                "content": msg.content
            }
            for msg in messages
        ]

    @staticmethod
    async def get_or_create_conversation(
        session: AsyncSession,
        user_id: str,
        conversation_id: Optional[int] = None
    ) -> Conversation:
        """
        Get existing conversation or create new one if not provided.

        Args:
            session: Database session
            user_id: Owner user identifier
            conversation_id: Optional existing conversation ID

        Returns:
            Conversation: Existing or newly created conversation

        Example:
            conversation = await ConversationService.get_or_create_conversation(
                session, user_id, request.conversation_id
            )
        """
        if conversation_id is not None:
            # Get existing conversation
            return await ConversationService.get_conversation(
                session, conversation_id, user_id
            )
        else:
            # Create new conversation
            return await ConversationService.create_conversation(session, user_id)
