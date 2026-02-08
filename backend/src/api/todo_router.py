"""
TodoRouter - REST API endpoints for advanced todo management.
"""
import json
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.services.todo_service import TodoService

router = APIRouter(prefix="/todos", tags=["todos"])


class TodoCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = None
    priority: str = Field(default="medium")
    due_date: Optional[str] = None
    tags: Optional[list[str]] = None
    is_recurring: bool = False
    recurrence_pattern: Optional[str] = None
    recurrence_interval: Optional[int] = None
    recurrence_end_date: Optional[str] = None
    reminder_enabled: bool = False
    reminder_offset_hours: Optional[int] = None


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[str] = None
    tags: Optional[list[str]] = None
    is_recurring: Optional[bool] = None
    recurrence_pattern: Optional[str] = None
    recurrence_interval: Optional[int] = None
    reminder_enabled: Optional[bool] = None
    reminder_offset_hours: Optional[int] = None


class TodoResponse(BaseModel):
    id: str
    user_id: str
    title: str
    description: Optional[str]
    status: str
    priority: str
    due_date: Optional[str]
    tags: Optional[list[str]]
    created_at: str
    updated_at: str
    is_recurring: bool
    recurrence_pattern: Optional[str]
    recurrence_interval: Optional[int]
    reminder_enabled: bool
    reminder_offset_hours: Optional[int]
    parent_id: Optional[str]


def _todo_to_response(todo) -> dict:
    tags = None
    if todo.tags:
        try:
            tags = json.loads(todo.tags)
        except (json.JSONDecodeError, TypeError):
            tags = []
    return {
        "id": str(todo.id),
        "user_id": str(todo.user_id),
        "title": todo.title,
        "description": todo.description,
        "status": todo.status,
        "priority": todo.priority,
        "due_date": todo.due_date.isoformat() if todo.due_date else None,
        "tags": tags,
        "created_at": todo.created_at.isoformat(),
        "updated_at": todo.updated_at.isoformat(),
        "is_recurring": todo.is_recurring,
        "recurrence_pattern": todo.recurrence_pattern,
        "recurrence_interval": todo.recurrence_interval,
        "reminder_enabled": todo.reminder_enabled,
        "reminder_offset_hours": todo.reminder_offset_hours,
        "parent_id": str(todo.parent_id) if todo.parent_id else None,
    }


# For now, extract user_id from a header (simplified for K8s deployment)
async def get_current_user_id() -> UUID:
    """Placeholder: returns a demo user ID. Replace with JWT auth extraction."""
    return UUID("00000000-0000-0000-0000-000000000001")


@router.post("", response_model=TodoResponse)
async def create_todo(
    body: TodoCreate,
    session: AsyncSession = Depends(get_session),
    user_id: UUID = Depends(get_current_user_id),
):
    service = TodoService(session)
    data = body.model_dump(exclude_none=True)
    todo = await service.create(user_id, data)
    return _todo_to_response(todo)


@router.get("", response_model=list[TodoResponse])
async def list_todos(
    status: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    session: AsyncSession = Depends(get_session),
    user_id: UUID = Depends(get_current_user_id),
):
    service = TodoService(session)
    todos = await service.list_todos(user_id, status=status, priority=priority, skip=skip, limit=limit)
    return [_todo_to_response(t) for t in todos]


@router.get("/{todo_id}", response_model=TodoResponse)
async def get_todo(
    todo_id: UUID,
    session: AsyncSession = Depends(get_session),
    user_id: UUID = Depends(get_current_user_id),
):
    service = TodoService(session)
    todo = await service.get_by_id(todo_id, user_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return _todo_to_response(todo)


@router.put("/{todo_id}", response_model=TodoResponse)
async def update_todo(
    todo_id: UUID,
    body: TodoUpdate,
    session: AsyncSession = Depends(get_session),
    user_id: UUID = Depends(get_current_user_id),
):
    service = TodoService(session)
    data = body.model_dump(exclude_none=True)
    todo = await service.update(todo_id, user_id, data)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return _todo_to_response(todo)


@router.delete("/{todo_id}")
async def delete_todo(
    todo_id: UUID,
    session: AsyncSession = Depends(get_session),
    user_id: UUID = Depends(get_current_user_id),
):
    service = TodoService(session)
    deleted = await service.delete(todo_id, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Todo deleted"}
