"""
Authentication Service
"""

from app.core.security import (
    create_access_token,
    verify_password,
)
from app.repositories.user_repository import UserRepository


class AuthService:
    """
    Authentication business logic.
    """

    def __init__(
        self,
        repository: UserRepository,
    ):
        self.repository = repository

    async def login(
        self,
        email: str,
        password: str,
    ) -> str:

        user = await self.repository.get_by_email(email)

        if user is None:
            raise ValueError("Invalid email or password.")

        if not verify_password(
            password,
            user.hashed_password,
        ):
            raise ValueError("Invalid email or password.")

        return create_access_token(
            subject=str(user.id),
        )