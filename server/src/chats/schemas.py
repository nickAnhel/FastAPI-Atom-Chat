import uuid
from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ChatCreate(BaseSchema):
    title: str
    is_private: bool = False
    members: list[uuid.UUID]


class ChatGet(BaseSchema):
    chat_id: uuid.UUID
    title: str
    is_private: bool
    owner_id: uuid.UUID
