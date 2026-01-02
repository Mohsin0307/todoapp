"""
Application Configuration - Environment Variables

Manages all environment variables using Pydantic BaseSettings for type safety and validation.
Loads from .env file in backend/ directory.
"""
from typing import List, Union

from pydantic import Field, PostgresDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database Configuration
    DATABASE_URL: PostgresDsn = Field(
        ...,
        description="PostgreSQL connection string (asyncpg driver)"
    )

    # JWT Authentication Configuration
    JWT_SECRET: str = Field(
        ...,
        min_length=32,
        description="Secret key for JWT signing (MUST match frontend BETTER_AUTH_SECRET)"
    )
    JWT_ALGORITHM: str = Field(
        default="HS256",
        description="JWT signing algorithm"
    )
    JWT_EXPIRATION_HOURS: int = Field(
        default=24,
        ge=1,
        le=168,  # Max 1 week
        description="JWT token expiration time in hours"
    )

    # CORS Configuration
    ALLOWED_ORIGINS: Union[List[str], str] = Field(
        default="http://localhost:3000",
        description="Allowed CORS origins (comma-separated in .env)"
    )

    # Server Configuration
    HOST: str = Field(
        default="0.0.0.0",
        description="Server host address"
    )
    PORT: int = Field(
        default=8000,
        ge=1024,
        le=65535,
        description="Server port"
    )
    LOG_LEVEL: str = Field(
        default="info",
        description="Logging level (debug, info, warning, error, critical)"
    )
    ENVIRONMENT: str = Field(
        default="development",
        description="Environment name (development, staging, production)"
    )

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def parse_allowed_origins(cls, v: Union[str, List[str]]) -> List[str]:
        """Parse comma-separated ALLOWED_ORIGINS into a list."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


# Global settings instance (singleton)
settings = Settings()
