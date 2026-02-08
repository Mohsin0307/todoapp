"""
NotificationService - Manages user notifications and reminders.
"""
from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.notification_model import Notification


class NotificationService:
    """Service for managing user notifications."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_id: UUID, data: dict) -> Notification:
        notification = Notification(user_id=user_id, **data)
        self.session.add(notification)
        await self.session.flush()
        return notification

    async def get_by_id(self, notification_id: UUID, user_id: UUID) -> Optional[Notification]:
        result = await self.session.execute(
            select(Notification).where(
                Notification.id == notification_id,
                Notification.user_id == user_id,
            )
        )
        return result.scalar_one_or_none()

    async def list_notifications(
        self,
        user_id: UUID,
        unread_only: bool = False,
        skip: int = 0,
        limit: int = 50,
    ) -> list[Notification]:
        query = select(Notification).where(Notification.user_id == user_id)
        if unread_only:
            query = query.where(Notification.is_read == False)
        query = query.order_by(Notification.created_at.desc()).offset(skip).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def mark_read(self, notification_id: UUID, user_id: UUID) -> Optional[Notification]:
        notification = await self.get_by_id(notification_id, user_id)
        if not notification:
            return None
        notification.is_read = True
        notification.read_at = datetime.utcnow()
        await self.session.flush()
        return notification

    async def mark_all_read(self, user_id: UUID) -> int:
        notifications = await self.list_notifications(user_id, unread_only=True, limit=1000)
        count = 0
        for n in notifications:
            n.is_read = True
            n.read_at = datetime.utcnow()
            count += 1
        await self.session.flush()
        return count

    async def unread_count(self, user_id: UUID) -> int:
        result = await self.session.execute(
            select(func.count(Notification.id)).where(
                Notification.user_id == user_id,
                Notification.is_read == False,
            )
        )
        return result.scalar_one()

    async def send_due_reminders(self) -> list[Notification]:
        """Find and deliver notifications that are due."""
        now = datetime.utcnow()
        result = await self.session.execute(
            select(Notification).where(
                Notification.is_delivered == False,
                Notification.scheduled_for <= now,
            )
        )
        due_notifications = list(result.scalars().all())
        for n in due_notifications:
            n.is_delivered = True
            n.sent_at = datetime.utcnow()
        await self.session.flush()
        return due_notifications
