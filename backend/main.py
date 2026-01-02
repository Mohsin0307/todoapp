"""
FastAPI Backend Application - Phase II Full-Stack Todo App

This is the main application entry point for the backend service.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import settings

# Create FastAPI application instance
app = FastAPI(
    title="Todo API",
    description="RESTful API for multi-user task management with JWT authentication",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

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
# Phase III: Database-backed AI Chat endpoint with Anthropic Claude & MCP tools
from src.api.chat_db import router as chat_router
app.include_router(chat_router, prefix="/api")  # Phase III: AI Chat endpoint
