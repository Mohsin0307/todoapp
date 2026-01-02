"""
Task Service - Business Logic for Task Management

Provides CRUD operations for tasks with user-scoped access and soft delete support.
"""
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import and_

from src.models.task import Task


class TaskService:
    """Service for task CRUD operations with user-scoped access."""

    @staticmethod
    async def list_tasks(
        session: AsyncSession,
        user_id: UUID,
        skip: int = 0,
        limit: int = 100,
        completed: Optional[bool] = None
    ) -> List[Task]:
        """
        List all active (non-deleted) tasks for a user with pagination and filtering.

        Args:
            session: Database session
            user_id: Owner user identifier
            skip: Number of records to skip (pagination offset)
            limit: Maximum number of records to return (max 100)
            completed: Filter by completion status (None = all tasks)

        Returns:
            List[Task]: List of tasks matching criteria

        Example:
            tasks = await TaskService.list_tasks(session, user_id, completed=False)
        """
        # Build query with user_id and soft delete filter
        query = select(Task).where(
            and_(
                Task.user_id == user_id,
                Task.deleted_at.is_(None)  # Only active tasks
            )
        )

        # Apply completed filter if specified
        if completed is not None:
            query = query.where(Task.completed == completed)

        # Apply ordering and pagination
        query = query.order_by(Task.created_at.desc()).offset(skip).limit(limit)

        # Execute query
        result = await session.execute(query)
        tasks = result.scalars().all()

        return list(tasks)

    @staticmethod
    async def create_task(
        session: AsyncSession,
        user_id: UUID,
        title: str,
        description: Optional[str] = None
    ) -> Task:
        """
        Create a new task for the user.

        Args:
            session: Database session
            user_id: Owner user identifier
            title: Task title (1-200 characters)
            description: Optional task description

        Returns:
            Task: Newly created task

        Raises:
            ValueError: If title is empty or exceeds 200 characters

        Example:
            task = await TaskService.create_task(
                session, user_id, "Complete docs", "Write API documentation"
            )
        """
        # Create new task instance
        task = Task(
            user_id=user_id,
            title=title,
            description=description,
            completed=False
        )

        # Add to session and flush to get ID
        session.add(task)
        await session.flush()
        await session.refresh(task)

        return task

    @staticmethod
    async def get_task(
        session: AsyncSession,
        task_id: UUID,
        user_id: UUID
    ) -> Task:
        """
        Get a single active task by ID (user-scoped).

        Args:
            session: Database session
            task_id: Task identifier
            user_id: Owner user identifier (for authorization)

        Returns:
            Task: The requested task

        Raises:
            HTTPException: 404 if task not found or doesn't belong to user

        Example:
            task = await TaskService.get_task(session, task_id, user_id)
        """
        # Query for task with user_id and soft delete check
        query = select(Task).where(
            and_(
                Task.id == task_id,
                Task.user_id == user_id,
                Task.deleted_at.is_(None)
            )
        )

        result = await session.execute(query)
        task = result.scalar_one_or_none()

        if task is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task {task_id} not found"
            )

        return task

    @staticmethod
    async def update_task(
        session: AsyncSession,
        task_id: UUID,
        user_id: UUID,
        title: Optional[str] = None,
        description: Optional[str] = None,
        completed: Optional[bool] = None
    ) -> Task:
        """
        Update an existing task (user-scoped, partial update).

        Args:
            session: Database session
            task_id: Task identifier
            user_id: Owner user identifier (for authorization)
            title: New title (optional)
            description: New description (optional)
            completed: New completion status (optional)

        Returns:
            Task: Updated task

        Raises:
            HTTPException: 404 if task not found or doesn't belong to user

        Example:
            task = await TaskService.update_task(
                session, task_id, user_id, title="Updated title", completed=True
            )
        """
        # Get existing task (raises 404 if not found)
        task = await TaskService.get_task(session, task_id, user_id)

        # Apply updates (only if provided)
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if completed is not None:
            task.completed = completed

        # Update timestamp
        task.updated_at = datetime.utcnow()

        # Flush changes
        await session.flush()
        await session.refresh(task)

        return task

    @staticmethod
    async def delete_task(
        session: AsyncSession,
        task_id: UUID,
        user_id: UUID
    ) -> None:
        """
        Soft delete a task (user-scoped).

        Args:
            session: Database session
            task_id: Task identifier
            user_id: Owner user identifier (for authorization)

        Raises:
            HTTPException: 404 if task not found or doesn't belong to user

        Example:
            await TaskService.delete_task(session, task_id, user_id)
        """
        # Get existing task (raises 404 if not found)
        task = await TaskService.get_task(session, task_id, user_id)

        # Set deleted_at timestamp (soft delete)
        task.deleted_at = datetime.utcnow()
        task.updated_at = datetime.utcnow()

        # Flush changes
        await session.flush()

    @staticmethod
    async def toggle_complete(
        session: AsyncSession,
        task_id: UUID,
        user_id: UUID
    ) -> Task:
        """
        Toggle the completion status of a task.

        Args:
            session: Database session
            task_id: Task identifier
            user_id: Owner user identifier (for authorization)

        Returns:
            Task: Updated task with toggled completion status

        Raises:
            HTTPException: 404 if task not found or doesn't belong to user

        Example:
            task = await TaskService.toggle_complete(session, task_id, user_id)
        """
        # Get existing task (raises 404 if not found)
        task = await TaskService.get_task(session, task_id, user_id)

        # Toggle completed status
        task.completed = not task.completed
        task.updated_at = datetime.utcnow()

        # Flush changes
        await session.flush()
        await session.refresh(task)

        return task
