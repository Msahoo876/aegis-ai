"""
Application Dependencies

Centralized dependency injection for repositories,
services, and database sessions.
"""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.services.user_service import UserService

from uuid import UUID

from fastapi import HTTPException, status

from app.core.security import (
    get_token_subject,
    oauth2_scheme,
)
from app.models.user import User

# ==========================================================
# Database
# ==========================================================

DatabaseSession = Annotated[
    AsyncSession,
    Depends(get_db),
]


# ==========================================================
# Repository Dependencies
# ==========================================================

def get_user_repository(
    db: DatabaseSession,
) -> UserRepository:
    """
    Return a UserRepository instance.
    """
    return UserRepository(db)


# ==========================================================
# Service Dependencies
# ==========================================================

def get_user_service(
    repository: Annotated[
        UserRepository,
        Depends(get_user_repository),
    ],
) -> UserService:
    """
    Return a UserService instance.
    """
    return UserService(repository)


def get_auth_service(
    repository: Annotated[
        UserRepository,
        Depends(get_user_repository),
    ],
) -> AuthService:
    """
    Return an AuthService instance.
    """
    return AuthService(repository)

async def get_current_user(
    token: Annotated[
        str,
        Depends(oauth2_scheme),
    ],
    repository: Annotated[
        UserRepository,
        Depends(get_user_repository),
    ],
) -> User:
    """
    Return the currently authenticated user.
    """

    try:

        user_id = UUID(
            get_token_subject(token)
        )

    except Exception as exc:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials.",
        ) from exc

    user = await repository.get_by_uuid(
        user_id
    )

    if user is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found.",
        )

    return user