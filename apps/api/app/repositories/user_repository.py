"""
User Repository
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.base import BaseRepository
from uuid import UUID


class UserRepository(BaseRepository[User]):
    """
    Repository for User entity.
    """

    def __init__(self, session: AsyncSession):
        super().__init__(session, User)

    async def get_by_email(
        self,
        email: str,
    ) -> User | None:

        result = await self.session.execute(
            select(User).where(
                User.email == email
            )
        )

        return result.scalar_one_or_none()

    async def get_by_uuid(
        self,
        user_id: UUID,
    ) -> User | None:
        """
        Retrieve a user by UUID.
        """
        return await self.get_by_id(user_id)

    async def get_by_username(
        self,
        username: str,
    ) -> User | None:

        result = await self.session.execute(
            select(User).where(
                User.username == username
            )
        )

        return result.scalar_one_or_none()