from fastapi import FastAPI

from src.auth.router import router as auth_router
from src.users.router import router as users_router
from src.users.exceptions import UserNotFound, UsernameAlreadyExists
from src.users.exc_handlers import user_not_found_handler, username_exists_handler


def include_routers(app: FastAPI) -> None:
    app.include_router(users_router)
    app.include_router(auth_router)


def add_exepton_handlers(app: FastAPI) -> None:
    app.add_exception_handler(UserNotFound, user_not_found_handler)  # type: ignore
    app.add_exception_handler(UsernameAlreadyExists, username_exists_handler)  # type: ignore
