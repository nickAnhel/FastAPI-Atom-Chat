import uuid
import datetime
from pydantic import BaseModel, ConfigDict

from src.users.schemas import UserGet


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class MessageCreateWS(BaseModel):
    content: str
    created_at: datetime.datetime


class MessageGetWS(MessageCreateWS):
    message_id: uuid.UUID
    username: str


class MessageCreate(BaseSchema):
    chat_id: int
    content: str
    user_id: uuid.UUID
    created_at: datetime.datetime


class MessageGet(MessageCreate):
    message_id: uuid.UUID


class MessageGetWithUser(MessageGet):
    user: UserGet
