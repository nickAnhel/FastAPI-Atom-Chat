from fastapi import FastAPI

from src.config import settings


def include_routes(app: FastAPI) -> None:
    from src.users.router import router as users_router

    app.include_router(users_router)


def add_exepton_handler(app: FastAPI) -> None:
    from src.users.exceptions import UserNotFound, UsernameAlreadyExists
    from src.users.exc_handlers import user_not_found_handler, username_exists_handler

    app.add_exception_handler(UserNotFound, user_not_found_handler)  # type: ignore
    app.add_exception_handler(UsernameAlreadyExists, username_exists_handler)  # type: ignore


app = FastAPI(
    title=settings.project.title,
    version=settings.project.version,
    description=settings.project.description,
    debug=settings.project.debug,
)


include_routes(app)
add_exepton_handler(app)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
