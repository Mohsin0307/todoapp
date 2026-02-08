"""
SearchService - Full-text search capabilities for todos.
"""
import json
from typing import Optional
from uuid import UUID

from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.todo_model import TodoItem


class SearchService:
    """Service for searching todo items with various criteria."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def search(
        self,
        user_id: UUID,
        query: Optional[str] = None,
        tags: Optional[list[str]] = None,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        has_due_date: Optional[bool] = None,
        is_recurring: Optional[bool] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> list[TodoItem]:
        stmt = select(TodoItem).where(TodoItem.user_id == user_id)

        if query:
            pattern = f"%{query}%"
            stmt = stmt.where(
                or_(
                    TodoItem.title.ilike(pattern),
                    TodoItem.description.ilike(pattern),
                )
            )

        if tags:
            # Search within JSON-serialized tags field
            for tag in tags:
                stmt = stmt.where(TodoItem.tags.ilike(f'%"{tag}"%'))

        if status:
            stmt = stmt.where(TodoItem.status == status)

        if priority:
            stmt = stmt.where(TodoItem.priority == priority)

        if has_due_date is True:
            stmt = stmt.where(TodoItem.due_date.isnot(None))
        elif has_due_date is False:
            stmt = stmt.where(TodoItem.due_date.is_(None))

        if is_recurring is not None:
            stmt = stmt.where(TodoItem.is_recurring == is_recurring)

        stmt = stmt.order_by(TodoItem.created_at.desc()).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
