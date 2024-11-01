import uuid
from typing import Annotated
from pydantic import Field

from src.schemas import BaseSchema


UsernameStr = Annotated[str, Field(min_length=1, max_length=32)]


class UserCreate(BaseSchema):
    username: UsernameStr
    password: str  # TODO: add password validation


class UserGet(BaseSchema):
    user_id: uuid.UUID
    username: UsernameStr
    is_deleted: bool
    is_blocked: bool
    is_admin: bool


class UserGetWithPassword(UserGet):
    hashed_password: str


class UserUpdate(BaseSchema):
    username: UsernameStr | None = None
