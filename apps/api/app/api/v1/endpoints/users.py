"""
User API Endpoints
"""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.v1.dependencies import get_user_service
from app.schemas.user import UserCreate, UserRead
from app.services.user_service import UserService

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post(
    "",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create User",
)
async def create_user(
    user: UserCreate,
    service: Annotated[
        UserService,
        Depends(get_user_service),
    ],
):
    """
    Create a new user.
    """

    try:
        return await service.create_user(user)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.get(
    "/{user_id}",
    response_model=UserRead,
    summary="Get User",
)
async def get_user(
    user_id: UUID,
    service: Annotated[
        UserService,
        Depends(get_user_service),
    ],
):
    """
    Retrieve a user by ID.
    """

    user = await service.get_user_by_id(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    return user