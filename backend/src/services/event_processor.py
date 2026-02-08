"""
EventProcessor - Handles incoming events from Kafka/Redpanda.

Processes events consumed from the todo-events topic and routes
them to appropriate handlers.
"""
import json
import logging
from datetime import datetime
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.models.event_model import Event

logger = logging.getLogger(__name__)


class EventProcessor:
    """Processes incoming events from the event stream."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self._handlers: dict = {
            "todo.created": self._handle_todo_created,
            "todo.updated": self._handle_todo_updated,
            "todo.completed": self._handle_todo_completed,
            "todo.deleted": self._handle_todo_deleted,
            "todo.recurring.triggered": self._handle_recurring_triggered,
            "reminder.sent": self._handle_reminder_sent,
        }

    async def process_event(self, event_data: dict) -> bool:
        """Process a single event from the stream."""
        event_type = event_data.get("type", "")
        handler = self._handlers.get(event_type)

        event = Event(
            id=event_data.get("id", ""),
            type=event_type,
            source=event_data.get("source", "unknown"),
            timestamp=datetime.fromisoformat(event_data.get("timestamp", datetime.utcnow().isoformat())),
            correlation_id=event_data.get("correlationId"),
            causation_id=event_data.get("causationId"),
            payload=json.dumps(event_data.get("payload", {})),
            user_id=event_data.get("userId"),
            todo_id=event_data.get("todoId"),
        )

        try:
            if handler:
                await handler(event)
            else:
                logger.warning("No handler for event type: %s", event_type)

            event.processed = True
            self.session.add(event)
            await self.session.flush()
            return True

        except Exception as e:
            event.retries += 1
            if event.retries >= event.max_retries:
                logger.error("Event %s exceeded max retries, dead-lettering: %s", event.id, str(e))
                event.processed = True  # Mark as processed to prevent retry loop
            else:
                logger.warning("Event %s processing failed (attempt %d): %s", event.id, event.retries, str(e))
            self.session.add(event)
            await self.session.flush()
            return False

    async def _handle_todo_created(self, event: Event):
        logger.info("Processing todo.created: %s", event.id)

    async def _handle_todo_updated(self, event: Event):
        logger.info("Processing todo.updated: %s", event.id)

    async def _handle_todo_completed(self, event: Event):
        logger.info("Processing todo.completed: %s", event.id)

    async def _handle_todo_deleted(self, event: Event):
        logger.info("Processing todo.deleted: %s", event.id)

    async def _handle_recurring_triggered(self, event: Event):
        logger.info("Processing todo.recurring.triggered: %s", event.id)

    async def _handle_reminder_sent(self, event: Event):
        logger.info("Processing reminder.sent: %s", event.id)
