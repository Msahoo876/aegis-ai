"""
Health Check Endpoints
"""
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_db
from app.core.config import settings

router = APIRouter()


@router.get(
    "/health/database",
    summary="Database Health Check",
)
async def database_health_check(
    db: AsyncSession = Depends(get_db),
):
    """
    Verify database connectivity.
    """

    result = await db.execute(text("SELECT 1"))

    return {
        "database": "connected",
        "result": result.scalar(),
    }