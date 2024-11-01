import uuid
from typing import Annotated
from pydantic import Field

from src.schemas import BaseSchema
from src.messages.schemas import MessageGetWithUser
from src.events.schemas import EventGetWithUsers


TitleStr = Annotated[str, Field(min_length=1, max_length=64)]


class ChatCreate(BaseSchema):
    title: TitleStr
    is_private: bool = False
    members: list[uuid.UUID]


class ChatGet(BaseSchema):
    chat_id: uuid.UUID
    title: TitleStr
    is_private: bool
    owner_id: uuid.UUID


class ChatUpdate(BaseSchema):
    title: TitleStr | None = None
    is_private: bool | None = None


class MessageHistoryItem(MessageGetWithUser):
    item_type: str = "message"


class EventHistoryItem(EventGetWithUsers):
    item_type: str = "event"
