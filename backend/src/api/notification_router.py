"""
NotificationRouter - API endpoints for notification management.
"""
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.services.notification_service import NotificationService
from src.api.todo_router import get_current_user_id

router = APIRouter(prefix="/notifications", tags=["notifications"])


class NotificationResponse(BaseModel):
    id: str
    type: str
    title: str
    message: str
    priority: str
    is_read: bool
    is_delivered: bool
    created_at: str
    scheduled_for: str | None
    sent_at: str | None
    read_at: str | None
    todo_id: str | None


def _notification_to_response(n) -> dict:
    return {
        "id": str(n.id),
        "type": n.type,
        "title": n.title,
        "message": n.message,
        "priority": n.priority,
        "is_read": n.is_read,
        "is_delivered": n.is_delivered,
        "created_at": n.created_at.isoformat(),
        "scheduled_for": n.scheduled_for.isoformat() if n.scheduled_for else None,
        "sent_at": n.sent_at.isoformat() if n.sent_at else None,
        "read_at": n.read_at.isoformat() if n.read_at else None,
        "todo_id": str(n.todo_id) if n.todo_id else None,
    }


@router.get("", response_model=list[NotificationResponse])
async def list_notifications(
    unread_only: bool = Query(False),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    session: AsyncSession = Depends(get_session),
    user_id: UUID = Depends(get_current_user_id),
):
    service = NotificationService(session)
    notifications = await service.list_notifications(user_id, unread_only=unread_only, skip=skip, limit=limit)
    return [_notification_to_response(n) for n in notifications]


@router.get("/unread-count")
async def unread_count(
    session: AsyncSession = Depends(get_session),
    user_id: UUID = Depends(get_current_user_id),
):
    service = NotificationService(session)
    count = await service.unread_count(user_id)
    return {"count": count}


@router.put("/{notification_id}/read", response_model=NotificationResponse)
async def mark_read(
    notification_id: UUID,
    session: AsyncSession = Depends(get_session),
    user_id: UUID = Depends(get_current_user_id),
):
    service = NotificationService(session)
    notification = await service.mark_read(notification_id, user_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return _notification_to_response(notification)


@router.put("/read-all")
async def mark_all_read(
    session: AsyncSession = Depends(get_session),
    user_id: UUID = Depends(get_current_user_id),
):
    service = NotificationService(session)
    count = await service.mark_all_read(user_id)
    return {"marked_read": count}
