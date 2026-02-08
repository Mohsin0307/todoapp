"""
RecurringTaskService - Handles recurring todo item creation and scheduling.
"""
import json
from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.todo_model import TodoItem


class RecurringTaskService:
    """Service for managing recurring todo items."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_recurring_todos(self, user_id: UUID) -> list[TodoItem]:
        result = await self.session.execute(
            select(TodoItem).where(
                TodoItem.user_id == user_id,
                TodoItem.is_recurring == True,
            ).order_by(TodoItem.created_at.desc())
        )
        return list(result.scalars().all())

    async def create_recurring_instance(self, template: TodoItem) -> Optional[TodoItem]:
        """Create a new instance of a recurring todo based on the template."""
        next_due = self._calculate_next_due(template)
        if not next_due:
            return None

        if template.recurrence_end_date and next_due > template.recurrence_end_date:
            return None

        instance = TodoItem(
            user_id=template.user_id,
            title=template.title,
            description=template.description,
            priority=template.priority,
            tags=template.tags,
            due_date=next_due,
            is_recurring=False,
            parent_id=template.id,
            reminder_enabled=template.reminder_enabled,
            reminder_offset_hours=template.reminder_offset_hours,
        )
        if template.reminder_enabled and template.reminder_offset_hours and next_due:
            instance.reminder_time = next_due - timedelta(hours=template.reminder_offset_hours)

        self.session.add(instance)
        await self.session.flush()
        return instance

    def _calculate_next_due(self, template: TodoItem) -> Optional[datetime]:
        """Calculate the next due date based on recurrence pattern."""
        base = template.due_date or datetime.utcnow()
        interval = template.recurrence_interval or 1
        pattern = template.recurrence_pattern

        if pattern == "daily":
            return base + timedelta(days=interval)
        elif pattern == "weekly":
            return base + timedelta(weeks=interval)
        elif pattern == "monthly":
            month = base.month + interval
            year = base.year + (month - 1) // 12
            month = (month - 1) % 12 + 1
            day = min(base.day, 28)
            return base.replace(year=year, month=month, day=day)
        elif pattern == "yearly":
            return base.replace(year=base.year + interval)
        return None

    async def process_due_recurring(self) -> list[TodoItem]:
        """Find and create instances for all recurring todos that are due."""
        now = datetime.utcnow()
        result = await self.session.execute(
            select(TodoItem).where(
                TodoItem.is_recurring == True,
                TodoItem.status != "cancelled",
            )
        )
        templates = result.scalars().all()
        created = []
        for template in templates:
            if template.due_date and template.due_date <= now:
                instance = await self.create_recurring_instance(template)
                if instance:
                    created.append(instance)
        return created
