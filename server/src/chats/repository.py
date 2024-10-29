from typing import Any
import uuid
from sqlalchemy import insert, select, update, delete, desc
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.models import UserModel
from src.chats.models import ChatModel, ChatUserM2M


class ChatRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self,
        data: dict[str, Any],
    ) -> ChatModel:
        stmt = (
            insert(ChatModel)
            .values(**data)
            .returning(ChatModel)
        )
        result = await self._session.execute(stmt)
        await self._session.commit()
        return result.scalar_one()

    async def get_single(
        self,
        **filters,
    ) -> ChatModel:
        query = (
            select(ChatModel)
            .filter_by(**filters)
        )

        result = await self._session.execute(query)
        return result.scalar_one()

    async def get_members(
        self,
        chat_id: uuid.UUID,
    ) -> list[UserModel]:
        query = (
            select(ChatModel)
            .filter_by(chat_id=chat_id)
            .options(joinedload(ChatModel.members))
        )

        result = await self._session.execute(query)
        chat =  result.unique().scalar_one()
        return chat.members

    async def get_multi(
        self,
        *,
        order: str,
        order_desc: bool,
        offset: int,
        limit: int,
    ) -> list[ChatModel]:
        query = (
            select(ChatModel)
            .filter_by(is_private=False)
            .order_by(desc(order) if order_desc else order)
            .offset(offset)
            .limit(limit)
        )
        result = await self._session.execute(query)
        return list(result.scalars().all())

    async def add_members(
        self,
        data: list[tuple[uuid.UUID, uuid.UUID]],
    ) -> int:
        stmt = (
            insert(ChatUserM2M)
            .values(data)
        )

        result = await self._session.execute(stmt)
        await self._session.commit()
        return result.rowcount

    async def remove_members(
        self,
        chat_id: uuid.UUID,
        members_ids: list[uuid.UUID],
    ) -> int:
        stmt = (
            delete(ChatUserM2M)
            .filter_by(chat_id=chat_id)
            .where(ChatUserM2M.user_id.in_(members_ids))
        )

        result = await self._session.execute(stmt)
        await self._session.commit()
        return result.rowcount

    async def update(
        self,
        chat_id: uuid.UUID,
        data: dict[str, Any],
    ) -> ChatModel:
        stmt = (
            update(ChatModel)
            .values(**data)
            .filter_by(chat_id=chat_id)
            .returning(ChatModel)
        )

        result = await self._session.execute(stmt)
        await self._session.commit()
        return result.scalar_one()

    async def delete(
        self,
        chat_id: uuid.UUID,
    ) -> int:
        stmt = (
            delete(ChatModel)
            .filter_by(chat_id=chat_id)
        )

        result = await self._session.execute(stmt)
        await self._session.commit()
        return result.rowcount

    async def search(
        self,
        *,
        text: str,
        order: str,
        order_desc: bool,
        offset: int,
        limit: int,
    ) -> list[ChatModel]:
        query = (
            select(ChatModel)
            .where(ChatModel.title.like(f'%{text}%'))
            .order_by(desc(order) if order_desc else order)
            .offset(offset)
            .limit(limit)
        )
        result = await self._session.execute(query)
        return list(result.scalars().all())
