from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete, desc

from src.users.models import UserModel


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self,
        data: dict[str, Any],
    ) -> UserModel:
        stmt = (
            insert(UserModel)
            .values(**data)
            .returning(UserModel)
        )

        result = await self._session.execute(stmt)
        await self._session.commit()
        return result.scalar_one()

    async def get_single(
        self,
        **filters,
    ) -> UserModel:
        query = (
            select(UserModel)
            .filter_by(**filters)
        )
        result = await self._session.execute(query)
        return result.scalar_one()

    async def get_multi(
        self,
        order: str,
        order_desc: bool,
        offset: int,
        limit: int,
    ) -> list[UserModel]:
        query = (
            select(UserModel)
            .order_by(desc(order) if order_desc else order)
            .offset(offset)
            .limit(limit)
        )
        result = await self._session.execute(query)
        return list(result.scalars().all())

    async def update(
        self,
        data: dict[str, Any],
        **filters,
    ) -> UserModel:
        stmt = (
            update(UserModel)
            .values(**data)
            .filter_by(**filters)
            .returning(UserModel)
        )

        result = await self._session.execute(stmt)
        await self._session.commit()
        return result.scalar_one()

    async def delete(
        self,
        **filters,
    ) -> int:
        stmt = (
            delete(UserModel)
            .filter_by(**filters)
        )

        result = await self._session.execute(stmt)
        await self._session.commit()
        return result.rowcount
