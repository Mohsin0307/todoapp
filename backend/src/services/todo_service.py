"""
TodoService - CRUD operations for advanced TodoItem model.
"""
import json
from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.todo_model import TodoItem


class TodoService:
    """Service for managing TodoItem entities."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_id: UUID, data: dict) -> TodoItem:
        tags = data.pop("tags", None)
        todo = TodoItem(user_id=user_id, **data)
        if tags and isinstance(tags, list):
            todo.tags = json.dumps(tags)
        self.session.add(todo)
        await self.session.flush()
        return todo

    async def get_by_id(self, todo_id: UUID, user_id: UUID) -> Optional[TodoItem]:
        result = await self.session.execute(
            select(TodoItem).where(
                TodoItem.id == todo_id,
                TodoItem.user_id == user_id,
            )
        )
        return result.scalar_one_or_none()

    async def list_todos(
        self,
        user_id: UUID,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> list[TodoItem]:
        query = select(TodoItem).where(TodoItem.user_id == user_id)
        if status:
            query = query.where(TodoItem.status == status)
        if priority:
            query = query.where(TodoItem.priority == priority)
        query = query.order_by(TodoItem.created_at.desc()).offset(skip).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def update(self, todo_id: UUID, user_id: UUID, data: dict) -> Optional[TodoItem]:
        todo = await self.get_by_id(todo_id, user_id)
        if not todo:
            return None
        tags = data.pop("tags", None)
        for key, value in data.items():
            if hasattr(todo, key):
                setattr(todo, key, value)
        if tags is not None:
            todo.tags = json.dumps(tags) if isinstance(tags, list) else tags
        todo.updated_at = datetime.utcnow()
        await self.session.flush()
        return todo

    async def delete(self, todo_id: UUID, user_id: UUID) -> bool:
        todo = await self.get_by_id(todo_id, user_id)
        if not todo:
            return False
        await self.session.delete(todo)
        await self.session.flush()
        return True

    async def count(self, user_id: UUID, status: Optional[str] = None) -> int:
        query = select(func.count(TodoItem.id)).where(TodoItem.user_id == user_id)
        if status:
            query = query.where(TodoItem.status == status)
        result = await self.session.execute(query)
        return result.scalar_one()
