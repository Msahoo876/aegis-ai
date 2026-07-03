"""
Authentication Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db

from app.api.v1.dependencies import get_db
# from app.db.session import get_session
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, Token
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth")


@router.post(
    "/login",
    response_model=Token,
    summary="Login",
)
async def login(
    data: LoginRequest,
    db: AsyncSession = Depends(get_db),
):

    repository = UserRepository(db)

    service = AuthService(repository)

    try:

        token = await service.login(
            data.email,
            data.password,
        )

        return Token(
            access_token=token,
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        )