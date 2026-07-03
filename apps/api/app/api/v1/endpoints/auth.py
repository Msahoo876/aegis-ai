"""
Authentication Endpoints
"""

from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from fastapi.security import OAuth2PasswordRequestForm

from app.api.v1.dependencies import (
    get_current_user,
    get_db,
)
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import Token
from app.schemas.user import UserRead
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/login",
    response_model=Token,
    summary="Login",
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db=Depends(get_db),
):
    """
    Authenticate a user and return a JWT access token.
    """

    repository = UserRepository(db)
    service = AuthService(repository)

    try:
        token = await service.login(
            form_data.username,   # username field contains the email
            form_data.password,
        )

        return Token(
            access_token=token,
            token_type="bearer",
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        ) from exc


@router.get(
    "/me",
    response_model=UserRead,
    summary="Current User",
)
async def current_user(
    user: Annotated[
        User,
        Depends(get_current_user),
    ],
):
    """
    Return the currently authenticated user.
    """

    return user