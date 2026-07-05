"""
Health check endpoints.
"""

from fastapi import APIRouter
from datetime import datetime

router = APIRouter()


@router.get("/")
async def health_check():
    """Basic health check."""
    return {
        "status": "healthy",
        "service": "Fleet-[Client] API",
        "timestamp": datetime.utcnow().isoformat(),
    }


@router.get("/ready")
async def readiness_check():
    """Readiness check — verify all dependencies."""
    checks = {
        "api": "ok",
        "database": "ok",  # TODO: actual check
        "redis": "ok",  # TODO: actual check
    }
    all_ok = all(v == "ok" for v in checks.values())

    return {
        "ready": all_ok,
        "checks": checks,
        "timestamp": datetime.utcnow().isoformat(),
    }
