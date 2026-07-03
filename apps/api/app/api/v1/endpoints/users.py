"""
User API Endpoints
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserRead
from app.services.user_service import UserService

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


def get_user_service(
    session: AsyncSession = Depends(get_db),
) -> UserService:
    """
    Dependency injection for UserService.
    """
    repository = UserRepository(session)
    return UserService(repository)


@router.post(
    "",
    response_model=UserRead,
    status_code=201,
)
async def create_user(
    user: UserCreate,
    service: UserService = Depends(get_user_service),
):
    """
    Create a new user.
    """

    try:
        return await service.create_user(user)

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc


@router.get(
    "/{user_id}",
    response_model=UserRead,
)
async def get_user(
    user_id: UUID,
    service: UserService = Depends(get_user_service),
):
    """
    Retrieve a user by ID.
    """

    user = await service.get_user_by_id(user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found.",
        )

    return user