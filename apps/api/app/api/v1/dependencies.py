"""
Shared API dependencies.
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

DatabaseSession = AsyncSession

__all__ = [
    "DatabaseSession",
    "get_db",
]