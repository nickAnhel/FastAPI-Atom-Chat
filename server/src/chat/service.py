from src.chat.repostory import MessageRepository
from src.chat.schemas import MessageGetWithUser, MessageCreate


class MessageService:
    def __init__(self, repostory: MessageRepository) -> None:
        self._repository = repostory

    async def add_message(
        self,
        message: MessageCreate,
    ) -> MessageGetWithUser:
        msg = await self._repository.create(data=message.model_dump())
        return MessageGetWithUser.model_validate(msg)

    async def get_list(
        self,
        *,
        chat_id: int,
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
