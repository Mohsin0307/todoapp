"""
SearchRouter - API endpoints for advanced search and filtering.
"""
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.services.search_service import SearchService
from src.api.todo_router import get_current_user_id, _todo_to_response

router = APIRouter(prefix="/todos/search", tags=["search"])


@router.get("")
async def search_todos(
    q: Optional[str] = Query(None, description="Search query for title/description"),
    tags: Optional[str] = Query(None, description="Comma-separated tags"),
    status: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    has_due_date: Optional[bool] = Query(None),
    is_recurring: Optional[bool] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    session: AsyncSession = Depends(get_session),
    user_id: UUID = Depends(get_current_user_id),
):
    service = SearchService(session)
    tag_list = [t.strip() for t in tags.split(",") if t.strip()] if tags else None
    results = await service.search(
        user_id=user_id,
        query=q,
        tags=tag_list,
        status=status,
        priority=priority,
        has_due_date=has_due_date,
        is_recurring=is_recurring,
        skip=skip,
        limit=limit,
    )
    return [_todo_to_response(t) for t in results]
