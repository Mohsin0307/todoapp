"""
MetricsRouter - Application metrics collection endpoint.

Provides a /metrics endpoint for Prometheus scraping and application health details.
"""
import time
from datetime import datetime

from fastapi import APIRouter

router = APIRouter(tags=["metrics"])

# Simple in-memory metrics counters
_start_time = time.time()
_request_count = 0
_error_count = 0


def increment_request_count():
    global _request_count
    _request_count += 1


def increment_error_count():
    global _error_count
    _error_count += 1


@router.get("/metrics")
async def get_metrics():
    """Application metrics endpoint for monitoring."""
    uptime = time.time() - _start_time
    return {
        "uptime_seconds": round(uptime, 2),
        "total_requests": _request_count,
        "total_errors": _error_count,
        "timestamp": datetime.utcnow().isoformat(),
        "service": "todo-backend",
        "version": "2.0.0",
    }


@router.get("/health/ready")
async def readiness_probe():
    """Kubernetes readiness probe."""
    return {"status": "ready", "timestamp": datetime.utcnow().isoformat()}


@router.get("/health/live")
async def liveness_probe():
    """Kubernetes liveness probe."""
    return {"status": "alive", "timestamp": datetime.utcnow().isoformat()}
