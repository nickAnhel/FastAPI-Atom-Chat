import uuid
from typing import Any
from sqlalchemy.orm import selectinload
from sqlalchemy import insert, select, update, delete, desc
from sqlalchemy.ext.asyncio import AsyncSession

from src.messages.models import MessageModel


class MessageRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self,
        data: dict[str, Any],
    ) -> MessageModel:
        stmt = (
            insert(MessageModel)
            .values(**data)
            .returning(MessageModel)
            .options(selectinload(MessageModel.user))
        )
        result = await self._session.execute(stmt)
        await self._session.commit()
        return result.scalar_one()

    async def get_single(
        self,
        **filters,
    ) -> MessageModel:
        query = (
            select(MessageModel)
            .filter_by(**filters)
            .options(selectinload(MessageModel.user))
        )

        result = await self._session.execute(query)
        return result.scalar_one()

    async def get_multi(
        self,
        chat_id: uuid.UUID,
        order: str,
        order_desc: bool,
        offset: int,
        limit: int,
    ) -> list[MessageModel]:
        query = (
            select(MessageModel)
            .filter_by(chat_id=chat_id)
            .order_by(desc(order) if order_desc else order)
            .offset(offset)
            .limit(limit)
            .options(selectinload(MessageModel.user))
        )

        result = await self._session.execute(query)
        return list(result.scalars().all())

    async def delete(
        self,
        **filters
    ) -> int:
        stmt = (
            delete(MessageModel)
            .filter_by(**filters)
        )

        result = await self._session.execute(stmt)
        await self._session.commit()
        return result.rowcount

    async def delete_multi(
        self,
        chat_id: uuid.UUID,
    ) -> int:
        stmt = (
            delete(MessageModel)
            .filter_by(chat_id=chat_id)
        )

        result = await self._session.execute(stmt)
        await self._session.commit()
        return result.rowcount


    async def update(
        self,
        data: dict[str, Any],
        **filters,
    ) -> MessageModel:
        stmt = (
            update(MessageModel)
            .values(**data)
            .filter_by(**filters)
            .returning(MessageModel)
        )

        result = await self._session.execute(stmt)
        await self._session.commit()
        return result.scalar_one()

    async def search(
        self,
        text: str,
        order: str,
        order_desc: bool,
        offset: int,
        limit: int,
        **filters,
    ) -> list[MessageModel]:
        query = (
            select(MessageModel)
            .filter_by(**filters)
            .where(
                MessageModel.content.like(f'%{text}%')
            )
            .order_by(desc(order) if order_desc else order)
            .offset(offset)
            .limit(limit)
            .options(selectinload(MessageModel.user))
        )

        result = await self._session.execute(query)
        return list(result.scalars().all())
