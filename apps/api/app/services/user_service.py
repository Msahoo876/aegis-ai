"""
User Service

Contains business logic for user management.
"""

from __future__ import annotations

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.core.security import hash_password


class UserService:
    """
    User business logic.
    """

    def __init__(
        self,
        repository: UserRepository,
    ):
        self.repository = repository

    async def get_user_by_id(
        self,
        user_id,
    ) -> User | None:
        """
        Retrieve a user by ID.
        """

        return await self.repository.get_by_id(user_id)

    async def get_user_by_email(
        self,
        email: str,
    ) -> User | None:
        """
        Retrieve a user by email.
        """

        return await self.repository.get_by_email(email)

    async def create_user(
        self,
        data: UserCreate,
    ) -> User:
        """
        Create a new user.
        """

        existing_email = await self.repository.get_by_email(
            data.email
        )

        if existing_email:
            raise ValueError(
                "Email already exists."
            )

        existing_username = (
            await self.repository.get_by_username(
                data.username
            )
        )

        if existing_username:
            raise ValueError(
                "Username already exists."
            )

        user = User(
            email=data.email,
            username=data.username,
            full_name=data.full_name,
            hashed_password=hash_password(data.password),
        )

        return await self.repository.create(user)