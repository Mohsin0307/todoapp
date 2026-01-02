"""
Health Check API Endpoint

Provides health status endpoint for monitoring and uptime checks.
"""
from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check() -> dict[str, str]:
    """
    Health check endpoint - no authentication required.

    Returns service status and version information.

    Returns:
        dict: Health status with service name, status, and version

    Example Response:
        {
            "service": "Todo API",
            "status": "healthy",
            "version": "2.0.0"
        }
    """
    return {
        "service": "Todo API",
        "status": "healthy",
        "version": "2.0.0"
    }
