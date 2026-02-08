"""
RecurringTaskProcessor - Scheduled task processing for recurring todos.

Handles the background processing of recurring tasks, creating new instances
when they become due.
"""
import logging
from datetime import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.todo_model import TodoItem
from src.services.recurring_task_service import RecurringTaskService
from src.services.event_publisher import EventPublisher
from src.services.notification_service import NotificationService

logger = logging.getLogger(__name__)


class RecurringTaskProcessor:
    """Processes recurring tasks and generates new instances."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.recurring_service = RecurringTaskService(session)
        self.notification_service = NotificationService(session)
        self.publisher = EventPublisher()

    async def process_all_due(self) -> dict:
        """Process all due recurring tasks and return summary."""
        created_items = await self.recurring_service.process_due_recurring()
        events_published = 0

        for item in created_items:
            event = self.publisher.create_event(
                event_type="todo.recurring.triggered",
                source="recurring-task-processor",
                payload={
                    "todo_id": str(item.id),
                    "title": item.title,
                    "parent_id": str(item.parent_id) if item.parent_id else None,
                },
                user_id=str(item.user_id),
                todo_id=str(item.id),
            )
            published = await self.publisher.publish(event)
            if published:
                events_published += 1

            if item.reminder_enabled and item.reminder_time:
                await self.notification_service.create(
                    user_id=item.user_id,
                    data={
                        "type": "reminder",
                        "title": f"Recurring task: {item.title}",
                        "message": f"A new instance of your recurring task '{item.title}' has been created.",
                        "priority": "normal",
                        "scheduled_for": item.reminder_time,
                        "todo_id": item.id,
                    },
                )

        logger.info(
            "Recurring task processing complete: %d items created, %d events published",
            len(created_items),
            events_published,
        )

        await self.publisher.close()
        return {
            "items_created": len(created_items),
            "events_published": events_published,
        }

    async def process_reminders(self) -> dict:
        """Send all due reminders."""
        sent = await self.notification_service.send_due_reminders()
        for notification in sent:
            event = self.publisher.create_event(
                event_type="reminder.sent",
                source="recurring-task-processor",
                payload={
                    "notification_id": str(notification.id),
                    "title": notification.title,
                },
                user_id=str(notification.user_id),
            )
            await self.publisher.publish(event)

        await self.publisher.close()
        return {"reminders_sent": len(sent)}
