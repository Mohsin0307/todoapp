"""
Tasks API Endpoints - RESTful Task Management

Provides CRUD operations for tasks with JWT authentication and user-scoped access.
"""
from typing import Annotated, List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.middleware.auth import get_current_user
from src.services.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["Tasks"])


# ============================================================================
# Request/Response Schemas
# ============================================================================

class TaskCreate(BaseModel):
    """Request schema for creating a task."""
    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(None, description="Optional task description")

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Complete project documentation",
                "description": "Write comprehensive README and API docs"
            }
        }
    }


class TaskUpdate(BaseModel):
    """Request schema for updating a task (partial update)."""
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(None, description="Task description")
    completed: Optional[bool] = Field(None, description="Completion status")

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Updated title",
                "completed": True
            }
        }
    }


class TaskResponse(BaseModel):
    """Response schema for task data."""
    id: UUID
    user_id: UUID
    title: str
    description: Optional[str]
    completed: bool
    created_at: str
    updated_at: str

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "user_id": "123e4567-e89b-12d3-a456-426614174001",
                "title": "Complete project documentation",
                "description": "Write comprehensive README and API docs",
                "completed": False,
                "created_at": "2025-12-31T10:00:00Z",
                "updated_at": "2025-12-31T10:00:00Z"
            }
        }
    }


# ============================================================================
# API Endpoints
# ============================================================================

@router.get("", response_model=List[TaskResponse])
async def list_tasks(
    user_id: Annotated[UUID, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of records"),
    completed: Optional[bool] = Query(None, description="Filter by completion status")
) -> List[TaskResponse]:
    """
    List all tasks for the authenticated user.

    Supports pagination and filtering by completion status.

    **Authentication required**: Bearer JWT token

    **Query Parameters**:
    - skip: Offset for pagination (default: 0)
    - limit: Maximum records to return (default: 100, max: 100)
    - completed: Filter by status - true (completed), false (active), or null (all)

    **Returns**: Array of task objects sorted by creation date (newest first)
    """
    tasks = await TaskService.list_tasks(
        session=session,
        user_id=user_id,
        skip=skip,
        limit=limit,
        completed=completed
    )

    return [
        TaskResponse(
            id=task.id,
            user_id=task.user_id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            created_at=task.created_at.isoformat(),
            updated_at=task.updated_at.isoformat()
        )
        for task in tasks
    ]


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    user_id: Annotated[UUID, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)]
) -> TaskResponse:
    """
    Create a new task for the authenticated user.

    **Authentication required**: Bearer JWT token

    **Request Body**: TaskCreate schema with title (required) and description (optional)

    **Returns**: Created task object with generated ID and timestamps
    """
    task = await TaskService.create_task(
        session=session,
        user_id=user_id,
        title=task_data.title,
        description=task_data.description
    )

    await session.commit()

    return TaskResponse(
        id=task.id,
        user_id=task.user_id,
        title=task.title,
        description=task.description,
        completed=task.completed,
        created_at=task.created_at.isoformat(),
        updated_at=task.updated_at.isoformat()
    )


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: UUID,
    user_id: Annotated[UUID, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)]
) -> TaskResponse:
    """
    Get a single task by ID.

    **Authentication required**: Bearer JWT token

    **Path Parameters**:
    - task_id: UUID of the task to retrieve

    **Returns**: Task object if found and belongs to authenticated user

    **Errors**:
    - 404: Task not found or doesn't belong to user
    """
    task = await TaskService.get_task(
        session=session,
        task_id=task_id,
        user_id=user_id
    )

    return TaskResponse(
        id=task.id,
        user_id=task.user_id,
        title=task.title,
        description=task.description,
        completed=task.completed,
        created_at=task.created_at.isoformat(),
        updated_at=task.updated_at.isoformat()
    )


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: UUID,
    task_data: TaskUpdate,
    user_id: Annotated[UUID, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)]
) -> TaskResponse:
    """
    Update an existing task (partial update).

    **Authentication required**: Bearer JWT token

    **Path Parameters**:
    - task_id: UUID of the task to update

    **Request Body**: TaskUpdate schema with optional title, description, completed fields

    **Returns**: Updated task object

    **Errors**:
    - 404: Task not found or doesn't belong to user
    """
    task = await TaskService.update_task(
        session=session,
        task_id=task_id,
        user_id=user_id,
        title=task_data.title,
        description=task_data.description,
        completed=task_data.completed
    )

    await session.commit()

    return TaskResponse(
        id=task.id,
        user_id=task.user_id,
        title=task.title,
        description=task.description,
        completed=task.completed,
        created_at=task.created_at.isoformat(),
        updated_at=task.updated_at.isoformat()
    )


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: UUID,
    user_id: Annotated[UUID, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)]
) -> None:
    """
    Soft delete a task (sets deleted_at timestamp).

    **Authentication required**: Bearer JWT token

    **Path Parameters**:
    - task_id: UUID of the task to delete

    **Returns**: No content (204) on success

    **Errors**:
    - 404: Task not found or doesn't belong to user

    **Note**: This is a soft delete - the task is marked as deleted but not removed from database
    """
    await TaskService.delete_task(
        session=session,
        task_id=task_id,
        user_id=user_id
    )

    await session.commit()


@router.patch("/{task_id}/complete", response_model=TaskResponse)
async def toggle_complete(
    task_id: UUID,
    user_id: Annotated[UUID, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)]
) -> TaskResponse:
    """
    Toggle the completion status of a task.

    **Authentication required**: Bearer JWT token

    **Path Parameters**:
    - task_id: UUID of the task to toggle

    **Returns**: Updated task object with toggled completion status

    **Errors**:
    - 404: Task not found or doesn't belong to user

    **Behavior**: Flips completed from true→false or false→true
    """
    task = await TaskService.toggle_complete(
        session=session,
        task_id=task_id,
        user_id=user_id
    )

    await session.commit()

    return TaskResponse(
        id=task.id,
        user_id=task.user_id,
        title=task.title,
        description=task.description,
        completed=task.completed,
        created_at=task.created_at.isoformat(),
        updated_at=task.updated_at.isoformat()
    )
