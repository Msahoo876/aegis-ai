"""
Generic Repository

Provides common CRUD operations for SQLAlchemy models.
"""

from __future__ import annotations

from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """
    Generic repository for CRUD operations.
    """

    def __init__(
        self,
        session: AsyncSession,
        model: type[ModelType],
    ):
        self.session = session
        self.model = model

    async def get_by_id(self, entity_id):
        """
        Retrieve an entity by primary key.
        """
        return await self.session.get(self.model, entity_id)

    async def get_all(self) -> list[ModelType]:
        """
        Return all entities.
        """
        result = await self.session.execute(
            select(self.model)
        )
        return list(result.scalars().all())

    async def create(self, obj: ModelType) -> ModelType:
        """
        Persist an entity.
        """
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def delete(self, obj: ModelType) -> None:
        """
        Delete an entity.
        """
        await self.session.delete(obj)
        await self.session.commit()