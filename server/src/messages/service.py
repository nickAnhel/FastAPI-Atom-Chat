import uuid
from sqlalchemy.exc import IntegrityError

from src.chats.exceptions import ChatNotFound

from src.messages.repository import MessageRepository
from src.messages.schemas import MessageGetWithUser, MessageCreate


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
