"""
FastAPI Backend Application - Phase III Chat-Only Mode

Simplified main.py that runs only the chat endpoint without database dependencies.
This allows testing the Claude AI integration while we resolve Python 3.14 compatibility issues.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config import settings

# Create FastAPI application instance
app = FastAPI(
    title="Todo AI Chat API",
    description="AI-Powered Task Management Chat (Chat-Only Mode)",
    version="3.0.0-chat",
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
        "name": "Todo AI Chat API",
        "version": "3.0.0-chat",
        "status": "operational (chat-only mode)",
        "docs": "/docs",
        "note": "Database features temporarily disabled due to Python 3.14 compatibility",
    }


# Register only chat router (no database dependencies)
from src.api.chat import router as chat_router
app.include_router(chat_router, prefix="/api")
