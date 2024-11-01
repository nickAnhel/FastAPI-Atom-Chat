import uuid
from typing import Any
from sqlalchemy import insert, select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.events.models import EventModel


class EventRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self,
        *,
        data: dict[str, Any],
    ) -> EventModel:
        stmt = (
            insert(EventModel)
            .values(**data)
            .returning(EventModel)
            .options(selectinload(EventModel.user))
        )

        result = await self._session.execute(stmt)
        await self._session.commit()
        return result.scalar_one()

    async def get_multi(
        self,
        *,
        chat_id: uuid.UUID,
        offset: int,
        limit: int,
    ) -> list[EventModel]:
        query = (
            select(EventModel)
            .filter_by(chat_id=chat_id)
            .order_by(EventModel.created_at.desc())
            .offset(offset)
            .limit(limit)
            .options(selectinload(EventModel.user))
        )
        result = await self._session.execute(query)
        return list(reversed((result.scalars().all())))
