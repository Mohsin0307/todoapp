"""
Auth Service - User Authentication and JWT Token Generation

Provides user registration, login, and JWT token generation.
"""
from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID

from fastapi import HTTPException, status
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.models.user import User

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    """Service for authentication operations."""

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a password using bcrypt.

        Args:
            password: Plain text password

        Returns:
            str: Hashed password

        Example:
            hashed = AuthService.hash_password("mypassword123")
        """
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verify a password against a hash.

        Args:
            plain_password: Plain text password
            hashed_password: Hashed password from database

        Returns:
            bool: True if password matches, False otherwise

        Example:
            is_valid = AuthService.verify_password("mypassword123", user.hashed_password)
        """
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_access_token(user_id: UUID) -> str:
        """
        Create a JWT access token for a user.

        Args:
            user_id: User identifier

        Returns:
            str: JWT token string

        Example:
            token = AuthService.create_access_token(user.id)
        """
        expire = datetime.utcnow() + timedelta(hours=settings.JWT_EXPIRATION_HOURS)

        payload = {
            "sub": str(user_id),  # Subject (user ID)
            "exp": expire,  # Expiration time
            "iat": datetime.utcnow(),  # Issued at
        }

        token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
        return token

    @staticmethod
    async def register_user(
        session: AsyncSession,
        email: str,
        password: str,
        name: str
    ) -> User:
        """
        Register a new user.

        Args:
            session: Database session
            email: User email (unique)
            password: Plain text password
            name: User display name

        Returns:
            User: Newly created user

        Raises:
            HTTPException: 400 if email already exists

        Example:
            user = await AuthService.register_user(session, "user@example.com", "pass123", "John")
        """
        # Check if email already exists
        query = select(User).where(User.email == email)
        result = await session.execute(query)
        existing_user = result.scalar_one_or_none()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Hash password
        hashed_password = AuthService.hash_password(password)

        # Create user
        user = User(
            email=email,
            hashed_password=hashed_password,
            name=name
        )

        session.add(user)
        await session.flush()
        await session.refresh(user)

        return user

    @staticmethod
    async def authenticate_user(
        session: AsyncSession,
        email: str,
        password: str
    ) -> Optional[User]:
        """
        Authenticate a user by email and password.

        Args:
            session: Database session
            email: User email
            password: Plain text password

        Returns:
            User: Authenticated user if credentials are valid, None otherwise

        Example:
            user = await AuthService.authenticate_user(session, "user@example.com", "pass123")
            if user:
                # Login successful
        """
        # Find user by email
        query = select(User).where(User.email == email)
        result = await session.execute(query)
        user = result.scalar_one_or_none()

        if not user:
            return None

        # Verify password
        if not AuthService.verify_password(password, user.hashed_password):
            return None

        return user
