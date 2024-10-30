import uuid
from sqlalchemy.exc import IntegrityError, NoResultFound

from src.chats.exceptions import ChatNotFound

from src.messages.exceptions import CantUpdateMessage, CantDeleteMessage
from src.messages.repository import MessageRepository
from src.messages.schemas import MessageGet, MessageGetWithUser, MessageCreate, MessageUpdate


class MessageService:
    def __init__(self, repostory: MessageRepository) -> None:
        self._repository = repostory

    async def create_message(
        self,
        message: MessageCreate,
    ) -> MessageGetWithUser:
        try:
            msg = await self._repository.create(data=message.model_dump())
            return MessageGetWithUser.model_validate(msg)
        except IntegrityError as exc:
            raise ChatNotFound(f"Chat with id '{message.chat_id}' not found") from exc

    async def get_messages(
        self,
        *,
        chat_id: uuid.UUID,
        order: str,
        order_desc: bool,
        offset: int,
        limit: int,
    ) -> list[MessageGetWithUser]:
        messages = await self._repository.get_multi(
            order=order,
            order_desc=order_desc,
            offset=offset,
            limit=limit,
            chat_id=chat_id,
        )
        return [MessageGetWithUser.model_validate(message) for message in messages]

    async def delete_message(
        self,
        *,
        user_id: uuid.UUID,
        message_id: uuid.UUID,
    ) -> None:
        if (
            await self._repository.delete(
                message_id=message_id,
                user_id=user_id,
            )
            != 1
        ):
            raise CantDeleteMessage(f"Message with id '{message_id}' and user_id '{user_id}' not found")

    async def delete_messages(
        self,
        *,
        chat_id: uuid.UUID,
    ) -> int:
        return await self._repository.delete_multi(chat_id=chat_id)

    async def udpate_message(
        self,
        *,
        data: MessageUpdate,
        message_id: uuid.UUID,
        user_id: uuid.UUID,
    ) -> MessageGet:
        try:
            message = await self._repository.update(
                data=data.model_dump(exclude_none=True),
                message_id=message_id,
                user_id=user_id,
            )
        except NoResultFound as exc:
            raise CantUpdateMessage(f"Message with id '{message_id}' and user_id '{user_id}' not found") from exc

        return MessageGet.model_validate(message)

    async def search_messages(
        self,
        *,
        chat_id: uuid.UUID,
        query: str,
        order: str,
        order_desc: bool,
        offset: int,
        limit: int,
    ) -> list[MessageGetWithUser]:
        messages = await self._repository.search(
            q=query,
            order=order,
            order_desc=order_desc,
            offset=offset,
            limit=limit,
            chat_id=chat_id,
        )
        return [MessageGetWithUser.model_validate(message) for message in messages]
