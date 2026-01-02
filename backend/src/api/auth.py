"""
Auth API Endpoints - User Registration and Login

Provides signup and login endpoints with JWT token generation.
"""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


# ============================================================================
# Request/Response Schemas
# ============================================================================

class SignupRequest(BaseModel):
    """Request schema for user registration."""
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=8, description="Password (minimum 8 characters)")
    name: str = Field(..., min_length=1, max_length=255, description="User display name")

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "user@example.com",
                "password": "securepassword123",
                "name": "John Doe"
            }
        }
    }


class LoginRequest(BaseModel):
    """Request schema for user login."""
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="Password")

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "user@example.com",
                "password": "securepassword123"
            }
        }
    }


class AuthResponse(BaseModel):
    """Response schema for successful authentication."""
    user: dict
    message: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "user": {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "email": "user@example.com",
                    "name": "John Doe"
                },
                "message": "Authentication successful"
            }
        }
    }


# ============================================================================
# API Endpoints
# ============================================================================

@router.post("/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def signup(
    signup_data: SignupRequest,
    response: Response,
    session: Annotated[AsyncSession, Depends(get_session)]
) -> AuthResponse:
    """
    Register a new user account.

    **Request Body**: SignupRequest with email, password, and name

    **Returns**: User object and sets JWT token in httpOnly cookie

    **Errors**:
    - 400: Email already registered
    - 422: Validation error (invalid email, password too short, etc.)
    """
    # Register user
    user = await AuthService.register_user(
        session=session,
        email=signup_data.email,
        password=signup_data.password,
        name=signup_data.name
    )

    await session.commit()

    # Generate JWT token
    token = AuthService.create_access_token(user.id)

    # Set httpOnly cookie with JWT token
    response.set_cookie(
        key="access_token",
        value=f"Bearer {token}",
        httponly=True,
        secure=False,  # Set to True in production with HTTPS
        samesite="lax",
        max_age=60 * 60 * 24 * 7,  # 7 days
    )

    return AuthResponse(
        user={
            "id": str(user.id),
            "email": user.email,
            "name": user.name
        },
        message="Registration successful"
    )


@router.post("/login", response_model=AuthResponse)
async def login(
    login_data: LoginRequest,
    response: Response,
    session: Annotated[AsyncSession, Depends(get_session)]
) -> AuthResponse:
    """
    Login with email and password.

    **Request Body**: LoginRequest with email and password

    **Returns**: User object and sets JWT token in httpOnly cookie

    **Errors**:
    - 401: Invalid credentials
    """
    # Authenticate user
    user = await AuthService.authenticate_user(
        session=session,
        email=login_data.email,
        password=login_data.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Generate JWT token
    token = AuthService.create_access_token(user.id)

    # Set httpOnly cookie with JWT token
    response.set_cookie(
        key="access_token",
        value=f"Bearer {token}",
        httponly=True,
        secure=False,  # Set to True in production with HTTPS
        samesite="lax",
        max_age=60 * 60 * 24 * 7,  # 7 days
    )

    return AuthResponse(
        user={
            "id": str(user.id),
            "email": user.email,
            "name": user.name
        },
        message="Login successful"
    )


@router.post("/logout")
async def logout(response: Response) -> dict:
    """
    Logout by clearing the JWT token cookie.

    **Returns**: Success message
    """
    # Clear the access_token cookie
    response.delete_cookie(
        key="access_token",
        httponly=True,
        samesite="lax"
    )

    return {"message": "Logout successful"}
