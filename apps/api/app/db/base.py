"""
Database Declarative Base

Defines the common base class for all SQLAlchemy ORM models.
"""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, MetaData, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# ==========================================================
# Naming Convention
# ==========================================================

metadata = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)


# ==========================================================
# Base Class
# ==========================================================

class Base(DeclarativeBase):
    """
    Base class for all ORM models.
    """

    metadata = metadata


# ==========================================================
# Timestamp Mixin
# ==========================================================

class TimestampMixin:
    """
    Adds created_at and updated_at timestamps.
    """

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


# ==========================================================
# UUID Primary Key Mixin
# ==========================================================

class UUIDPrimaryKeyMixin:
    """
    Adds a UUID primary key named 'id'.
    """

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )