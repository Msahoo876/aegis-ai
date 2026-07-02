"""
Health Check Endpoints
"""

from fastapi import APIRouter

from app.core.config import settings

router = APIRouter()


@router.get(
    "/health",
    summary="Application Health Check",
)
async def health_check():
    """
    Returns application health status.
    """

    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT.value,
    }