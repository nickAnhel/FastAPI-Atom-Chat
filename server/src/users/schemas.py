import uuid
from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field


UsernameStr = Annotated[str, Field(min_length=1, max_length=32)]


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    username: UsernameStr
    password: str  # TODO: add password validation


class UserGet(UserBase):
    user_id: uuid.UUID
    username: UsernameStr


class UserGetWithPassword(UserGet):
    hashed_password: str


class UserUpdate(UserBase):
    username: UsernameStr
