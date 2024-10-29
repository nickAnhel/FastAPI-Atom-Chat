from fastapi import FastAPI

from src.auth.router import router as auth_router
from src.messages.router import router as messages_router
from src.users.router import router as users_router
from src.users.exceptions import UserNotFound, UsernameAlreadyExists
from src.users.exc_handlers import user_not_found_handler, username_exists_handler
from src.chats.router import router as chats_router
from src.chats.exceptions import (
    CantAddMembers,
    ChatNotFound,
    PermissionDenied,
    AlreadyInChat,
)
from src.chats.exc_handlers import (
    chat_not_found_handler,
    permission_denied_handler,
    already_in_chat_handler,
    cant_add_members_handler,
)
from src.messages.exceptions import CantUpdateMessage
from src.messages.exc_handlers import cant_update_message_handler


def include_routers(app: FastAPI) -> None:
    app.include_router(users_router)
    app.include_router(auth_router)
    app.include_router(messages_router)
    app.include_router(chats_router)


def add_exepton_handlers(app: FastAPI) -> None:
    app.add_exception_handler(UserNotFound, user_not_found_handler)  # type: ignore
    app.add_exception_handler(UsernameAlreadyExists, username_exists_handler)  # type: ignore

    app.add_exception_handler(ChatNotFound, chat_not_found_handler)  # type: ignore
    app.add_exception_handler(PermissionDenied, permission_denied_handler)  # type: ignore
    app.add_exception_handler(AlreadyInChat, already_in_chat_handler)  # type: ignore
    app.add_exception_handler(CantAddMembers, cant_add_members_handler)  # type: ignore

    app.add_exception_handler(CantUpdateMessage, cant_update_message_handler)  # type: ignore
