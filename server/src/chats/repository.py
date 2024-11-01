from typing import Any
import uuid
from sqlalchemy import insert, select, update, delete, union , desc, or_, func
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.models import UserModel
from src.messages.models import MessageModel
from src.events.models import EventModel
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

    async def history(
        self,
        *,
        chat_id: uuid.UUID,
        offset: int,
        limit: int,
    ) -> list[MessageModel | EventModel]:
        msgs_query = (
            select(MessageModel.message_id.label("id"), MessageModel.created_at)
            .filter_by(chat_id=chat_id)
        )

        events_query = (
            select(EventModel.event_id.label("id"), EventModel.created_at)
            .filter_by(chat_id=chat_id)
        )

        union_query = (
            union(
                msgs_query,
                events_query,
            )
            .order_by(desc("created_at"))
            .offset(offset)
            .limit(limit)
            .cte()
        )

        q1  = (
            select(MessageModel)
            .join(union_query, MessageModel.message_id == union_query.c.id)
            .options(selectinload(MessageModel.user))
        )

        q2 = (
            select(EventModel)
            .join(union_query, EventModel.event_id == union_query.c.id)
            .options(selectinload(EventModel.user))
        )

        messages: list[MessageModel] = (await self._session.execute(q1)).scalars().all()  # type: ignore
        events: list[EventModel] = (await self._session.execute(q2)).scalars().all()  # type: ignore

        history = messages + events
        return sorted(history, key=lambda item: item.created_at)

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
        user_id: uuid.UUID,
        q: str,
        offset: int,
        limit: int,
    ) -> list[ChatModel]:
        subquery = (
            select(ChatModel.chat_id)
            .where(
                ChatModel.title.bool_op("%")(q),
                or_(
                    ChatModel.is_private == False,
                    ChatModel.members.contains(UserModel(user_id=user_id)),
                ),
            )
            .distinct()
            .subquery()
        )

        query = (
            select(ChatModel)
            .join(subquery, ChatModel.chat_id == subquery.c.chat_id)
            .order_by(
                func.similarity(ChatModel.title, q).desc(),
            )
            .offset(offset)
            .limit(limit)
        )

        result = await self._session.execute(query)
        return list(result.scalars().all())
