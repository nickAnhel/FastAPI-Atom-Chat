import uuid
from typing import Any
from sqlalchemy.orm import selectinload
from sqlalchemy import insert, select, desc
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
