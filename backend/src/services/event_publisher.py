"""
EventPublisher - Publishes events to Kafka/Redpanda via Dapr or direct.

Supports both Dapr sidecar and direct HTTP fallback for local development.
"""
import json
import logging
from datetime import datetime
from typing import Optional
from uuid import uuid4

import httpx

from src.models.event_model import Event

logger = logging.getLogger(__name__)

DAPR_HTTP_PORT = 3500
DAPR_PUBSUB_NAME = "todo-pubsub"


class EventPublisher:
    """Publishes events to Kafka/Redpanda via Dapr pubsub."""

    def __init__(self, dapr_url: Optional[str] = None):
        self.dapr_url = dapr_url or f"http://localhost:{DAPR_HTTP_PORT}"
        self._client: Optional[httpx.AsyncClient] = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(timeout=10.0)
        return self._client

    def create_event(
        self,
        event_type: str,
        source: str,
        payload: dict,
        user_id: Optional[str] = None,
        todo_id: Optional[str] = None,
        causation_id: Optional[str] = None,
    ) -> Event:
        return Event(
            id=str(uuid4()),
            type=event_type,
            source=source,
            timestamp=datetime.utcnow(),
            correlation_id=str(uuid4()),
            causation_id=causation_id,
            payload=json.dumps(payload),
            user_id=user_id,
            todo_id=todo_id,
        )

    async def publish(self, event: Event, topic: str = "todo-events") -> bool:
        """Publish an event to the specified topic via Dapr."""
        try:
            client = await self._get_client()
            url = f"{self.dapr_url}/v1.0/publish/{DAPR_PUBSUB_NAME}/{topic}"
            data = {
                "id": event.id,
                "type": event.type,
                "source": event.source,
                "timestamp": event.timestamp.isoformat(),
                "correlationId": event.correlation_id,
                "causationId": event.causation_id,
                "payload": json.loads(event.payload) if event.payload else {},
                "userId": event.user_id,
                "todoId": event.todo_id,
            }
            response = await client.post(url, json=data)
            if response.status_code in (200, 204):
                logger.info("Event published: %s -> %s", event.type, topic)
                return True
            logger.warning("Failed to publish event: %s, status: %d", event.type, response.status_code)
            return False
        except httpx.ConnectError:
            logger.warning("Dapr sidecar not available, event not published: %s", event.type)
            return False
        except Exception as e:
            logger.error("Error publishing event %s: %s", event.type, str(e))
            return False

    async def close(self):
        if self._client and not self._client.is_closed:
            await self._client.aclose()
