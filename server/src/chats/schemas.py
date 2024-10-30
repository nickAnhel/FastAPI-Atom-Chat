import uuid
from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field


TitleStr = Annotated[str, Field(min_length=1, max_length=64)]


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


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
