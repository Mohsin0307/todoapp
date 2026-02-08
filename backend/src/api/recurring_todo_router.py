"""
RecurringTodoRouter - API endpoints for recurring task management.
"""
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.services.recurring_task_service import RecurringTaskService
from src.api.todo_router import get_current_user_id, _todo_to_response

router = APIRouter(prefix="/todos/recurring", tags=["recurring-todos"])


@router.get("")
async def list_recurring_todos(
    session: AsyncSession = Depends(get_session),
    user_id: UUID = Depends(get_current_user_id),
):
    service = RecurringTaskService(session)
    todos = await service.get_recurring_todos(user_id)
    return [_todo_to_response(t) for t in todos]


@router.post("/{todo_id}/generate")
async def generate_recurring_instance(
    todo_id: UUID,
    session: AsyncSession = Depends(get_session),
    user_id: UUID = Depends(get_current_user_id),
):
    from src.services.todo_service import TodoService
    todo_service = TodoService(session)
    template = await todo_service.get_by_id(todo_id, user_id)
    if not template:
        raise HTTPException(status_code=404, detail="Recurring todo not found")
    if not template.is_recurring:
        raise HTTPException(status_code=400, detail="Todo is not recurring")

    service = RecurringTaskService(session)
    instance = await service.create_recurring_instance(template)
    if not instance:
        raise HTTPException(status_code=400, detail="Could not generate next instance")
    return _todo_to_response(instance)


@router.post("/process-due")
async def process_due_recurring(
    session: AsyncSession = Depends(get_session),
):
    service = RecurringTaskService(session)
    created = await service.process_due_recurring()
    return {"created": len(created), "items": [_todo_to_response(t) for t in created]}
