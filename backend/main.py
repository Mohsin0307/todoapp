"""
FastAPI Backend Application - Phase II Full-Stack Todo App

This is the main application entry point for the backend service.
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from src.config import settings

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

# Create FastAPI application instance
app = FastAPI(
    title="Todo API",
    description="RESTful API for multi-user task management with JWT authentication",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Register rate limiter with app state
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint - API information."""
    return {
        "name": "Todo API",
        "version": "2.0.0",
        "status": "operational",
        "docs": "/docs",
    }


# Register API routers
from src.api.health import router as health_router
from src.api.tasks import router as tasks_router
from src.api.auth import router as auth_router

app.include_router(health_router)
app.include_router(auth_router, prefix="/api")
app.include_router(tasks_router, prefix="/api")
# Phase III: Database-backed AI Chat endpoint with OpenAI GPT & function calling
from src.api.chat_db import router as chat_router
app.include_router(chat_router, prefix="/api")

# Phase V: Cloud deployment - Advanced todo, recurring tasks, events
from src.api.todo_router import router as todo_router
from src.api.recurring_todo_router import router as recurring_todo_router
from src.api.event_router import router as event_router

app.include_router(todo_router, prefix="/api")
app.include_router(recurring_todo_router, prefix="/api")
app.include_router(event_router, prefix="/api")

# Phase V: Notifications, search, and WebSocket
from src.api.notification_router import router as notification_router
from src.api.search_router import router as search_router
from src.api.websocket_router import router as ws_router

app.include_router(notification_router, prefix="/api")
app.include_router(search_router, prefix="/api")
app.include_router(ws_router)

# Phase V: Metrics and monitoring
from src.api.metrics_router import router as metrics_router
app.include_router(metrics_router)

# Structured logging middleware
from src.middleware.logging_middleware import StructuredLoggingMiddleware
app.add_middleware(StructuredLoggingMiddleware)
