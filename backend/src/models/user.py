"""
User Model - SQLModel Definition

Represents a user entity for authentication.
"""
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    """
    User entity for authentication.

    Attributes:
        id: Unique user identifier (UUID)
        email: User email (unique, indexed)
        name: User display name
        hashed_password: Bcrypt hashed password
        created_at: User creation timestamp
        updated_at: Last modification timestamp
    """

    __tablename__ = "users"

    # Primary Key
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        nullable=False,
        description="Unique user identifier"
    )

    # Authentication
    email: str = Field(
        unique=True,
        index=True,
        nullable=False,
        max_length=255,
        description="User email address (unique)"
    )

    hashed_password: str = Field(
        nullable=False,
        description="Bcrypt hashed password"
    )

    # Profile
    name: str = Field(
        nullable=False,
        max_length=255,
        description="User display name"
    )

    # Timestamps
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="User creation timestamp"
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Last modification timestamp"
    )

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "email": "user@example.com",
                "name": "John Doe",
                "created_at": "2025-12-31T10:00:00Z",
                "updated_at": "2025-12-31T10:00:00Z",
            }
        }
