"""
Authentication Middleware - JWT Token Verification

Provides FastAPI dependency for extracting and validating user identity from JWT tokens.
Supports both httpOnly cookie and Authorization header.
"""
from typing import Annotated, Optional
from uuid import UUID

from fastapi import Cookie, Depends, HTTPException, Request, status
from jose import JWTError, jwt

from src.config import settings


async def get_current_user(
    request: Request,
    access_token: Annotated[Optional[str], Cookie()] = None
) -> UUID:
    """
    Extract and validate user_id from JWT token (cookie or Authorization header).

    Args:
        request: FastAPI request object
        access_token: JWT token from httpOnly cookie

    Returns:
        UUID: Authenticated user identifier

    Raises:
        HTTPException: 401 if token is invalid, expired, or missing user_id

    Usage:
        @app.get("/protected")
        async def protected_route(user_id: UUID = Depends(get_current_user)):
            return {"user_id": str(user_id)}
    """
    token = None

    # Try to get token from cookie first (httpOnly cookie from auth endpoints)
    if access_token:
        # Cookie format: "Bearer {token}"
        if access_token.startswith("Bearer "):
            token = access_token[7:]  # Remove "Bearer " prefix
        else:
            token = access_token

    # Fallback to Authorization header (for API testing with tools like Postman)
    if not token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header[7:]  # Remove "Bearer " prefix

    # Define the credentials exception
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not token:
        raise credentials_exception

    try:
        # Decode JWT token
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )

        # Extract user_id from token payload
        # Uses "sub" (subject) claim for user ID
        user_id_str: str | None = payload.get("sub")

        if user_id_str is None:
            raise credentials_exception

        # Convert to UUID
        user_id = UUID(user_id_str)

    except JWTError:
        # Token is invalid, expired, or malformed
        raise credentials_exception
    except ValueError:
        # user_id is not a valid UUID
        raise credentials_exception

    return user_id
