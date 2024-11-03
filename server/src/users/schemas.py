import uuid
from typing import Annotated
from pydantic import Field, field_validator


from src.schemas import BaseSchema


UsernameStr = Annotated[str, Field(min_length=1, max_length=32)]
PasswordStr = Annotated[str, Field(min_length=8, max_length=20, examples=["string12"])]


class UserCreate(BaseSchema):
    username: UsernameStr
    password: PasswordStr

    @field_validator("password")
    @classmethod
    def password_validation(cls, v):
        # if len(v) < 8:
        #     raise ValueError("Password must be at least 8 characters long")
        if not any(char.isdigit() for char in v):
            raise ValueError("Password must contain at least one digit")
        if not any(char.isalpha() for char in v):
            raise ValueError("Password must contain at least one letter")

        return v


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
