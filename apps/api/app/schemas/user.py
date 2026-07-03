"""
User Pydantic Schemas

Defines request and response models for the User entity.
"""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# ==========================================================
# Base Schema
# ==========================================================

class UserBase(BaseModel):
    """
    Shared user fields.
    """

    email: EmailStr

    username: str = Field(
        min_length=3,
        max_length=100,
    )

    full_name: str = Field(
        min_length=2,
        max_length=255,
    )


# ==========================================================
# Create User
# ==========================================================

class UserCreate(UserBase):
    """
    Schema for creating a new user.
    """

    password: str = Field(
        min_length=8,
        max_length=128,
    )


# ==========================================================
# Update User
# ==========================================================

class UserUpdate(BaseModel):
    """
    Schema for updating a user.
    """

    email: EmailStr | None = None

    username: str | None = Field(
        default=None,
        min_length=3,
        max_length=100,
    )

    full_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=255,
    )


# ==========================================================
# Login
# ==========================================================

class UserLogin(BaseModel):
    """
    Login schema.
    """

    email: EmailStr

    password: str


# ==========================================================
# Response Schema
# ==========================================================

class UserRead(UserBase):
    """
    User response schema.
    """

    id: UUID

    is_active: bool

    is_superuser: bool

    is_verified: bool

    last_login: datetime | None

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )