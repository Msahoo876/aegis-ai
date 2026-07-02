"""
Database Session Configuration

Provides the SQLAlchemy async engine,
session factory, and database dependency.
"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings

# ==========================================================
# Database URL
# ==========================================================

DATABASE_URL = str(settings.DATABASE_URL).replace(
    "postgresql://",
    "postgresql+asyncpg://",
    1,
)

# ==========================================================
# Async Engine
# ==========================================================

engine = create_async_engine(
    DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
)

# ==========================================================
# Session Factory
# ==========================================================

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)

# ==========================================================
# Database Dependency
# ==========================================================

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency that provides
    an async database session.
    """

    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()