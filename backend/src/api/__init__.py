"""
API Package - REST Endpoints

Exports FastAPI routers for all API endpoints.
"""
from src.api.health import router as health_router
from src.api.tasks import router as tasks_router
from src.api.auth import router as auth_router

__all__ = ["health_router", "tasks_router", "auth_router"]
