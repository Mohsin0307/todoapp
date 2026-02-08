"""
EventRouter - API endpoints for event-driven operations.
"""
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.services.event_publisher import EventPublisher
from src.services.dapr_integration import DaprIntegrationService

router = APIRouter(prefix="/events", tags=["events"])


class PublishEventRequest(BaseModel):
    type: str
    source: str
    payload: dict = {}
    user_id: str | None = None
    todo_id: str | None = None


@router.post("/publish")
async def publish_event(body: PublishEventRequest):
    publisher = EventPublisher()
    event = publisher.create_event(
        event_type=body.type,
        source=body.source,
        payload=body.payload,
        user_id=body.user_id,
        todo_id=body.todo_id,
    )
    success = await publisher.publish(event)
    await publisher.close()
    return {"published": success, "event_id": event.id}


@router.get("/health/dapr")
async def dapr_health():
    dapr = DaprIntegrationService()
    healthy = await dapr.health_check()
    await dapr.close()
    return {"dapr_healthy": healthy}


@router.post("/subscribe")
async def subscribe_handler(body: dict):
    """Dapr subscription handler endpoint."""
    return {"status": "SUCCESS"}


@router.get("/dapr/subscribe")
async def dapr_subscriptions():
    """Returns the list of subscriptions for Dapr to register."""
    return [
        {
            "pubsubname": "todo-pubsub",
            "topic": "todo-events",
            "route": "/api/events/subscribe",
        }
    ]
