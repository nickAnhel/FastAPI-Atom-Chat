import uuid
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select, insert, update, desc, func

from src.chats.models import ChatModel
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
        query = select(UserModel).filter_by(**filters)
        result = await self._session.execute(query)
        return result.scalar_one()

    async def get_multi(
        self,
        *,
        order: str,
        order_desc: bool,
        offset: int,
        limit: int,
    ) -> list[UserModel]:
        query = (
            select(UserModel)
            .filter_by(
                is_deleted=False,
                is_blocked=False,
            )
            .order_by(desc(order) if order_desc else order)
            .offset(offset)
            .limit(limit)
        )
        result = await self._session.execute(query)
        return list(result.scalars().all())

    async def search(
        self,
        *,
        q: str,
        user_id: uuid.UUID,
        offset: int,
        limit: int,
    ) -> list[UserModel]:
        query = (
            select(UserModel)
            .where(
                UserModel.username.bool_op("%")(q),
                UserModel.user_id != user_id,
                UserModel.is_deleted == False,
                UserModel.is_blocked == False,
            )
            .order_by(func.similarity(UserModel.username, q).desc())
            .offset(offset)
            .limit(limit)
        )

        result = await self._session.execute(query)
        return list(result.scalars().all())

    async def get_joined_chats(
        self,
        **filters,
    ) -> list[ChatModel]:
        query = (
            select(UserModel)
            .filter_by(**filters)
            .options(selectinload(UserModel.joined_chats))
        )
        result = await self._session.execute(query)
        user = result.scalar_one()
        return user.joined_chats

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

    async def mark_deleted(
        self,
        **filters,
    ) -> UserModel:
        stmt = (
            update(UserModel)
            .values(is_deleted=True)
            .filter_by(**filters)
            .returning(UserModel)
        )

        result = await self._session.execute(stmt)
        await self._session.commit()
        return result.scalar_one()

    async def mark_restored(
        self,
        **filters,
    ) -> UserModel:
        stmt = (
            update(UserModel)
            .values(is_deleted=False)
            .filter_by(**filters)
            .returning(UserModel)
        )

        result = await self._session.execute(stmt)
        await self._session.commit()
        return result.scalar_one()

    async def mark_blocked(
        self,
        **filters,
    ) -> UserModel:
        stmt = (
            update(UserModel)
            .values(is_blocked=True)
            .filter_by(**filters)
            .returning(UserModel)
        )

        result = await self._session.execute(stmt)
        await self._session.commit()
        return result.scalar_one()

    async def mark_unblocked(
        self,
        **filters,
    ) -> UserModel:
        stmt = (
            update(UserModel)
            .values(is_blocked=False)
            .filter_by(**filters)
            .returning(UserModel)
        )

        result = await self._session.execute(stmt)
        await self._session.commit()
        return result.scalar_one()
