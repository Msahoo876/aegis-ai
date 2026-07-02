"""
Alembic Environment Configuration

Configures Alembic to work with the Aegis AI
SQLAlchemy async engine.
"""

from __future__ import annotations

import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from app.core.config import settings
from app.db.base import Base
import app.models

# ==========================================================
# Alembic Config
# ==========================================================

config = context.config

# ==========================================================
# Logging
# ==========================================================

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ==========================================================
# Database URL
# ==========================================================

DATABASE_URL = (
    str(settings.DATABASE_URL)
    .replace(
        "postgresql://",
        "postgresql+asyncpg://",
        1,
    )
)

# Escape % characters for ConfigParser
config.set_main_option(
    "sqlalchemy.url",
    DATABASE_URL.replace("%", "%%"),
)

# ==========================================================
# Metadata
# ==========================================================

target_metadata = Base.metadata

# ==========================================================
# Offline Migrations
# ==========================================================


def run_migrations_offline() -> None:
    """Run migrations in offline mode."""

    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


# ==========================================================
# Online Migrations
# ==========================================================


def do_run_migrations(connection: Connection) -> None:
    """Run migrations using an active connection."""

    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Create async engine and execute migrations."""

    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Entry point for online migrations."""

    asyncio.run(run_async_migrations())


# ==========================================================
# Entrypoint
# ==========================================================

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()