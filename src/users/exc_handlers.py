from fastapi import HTTPException, status

from src.users.exceptions import UserNotFound, UsernameAlreadyExists


async def user_not_found_handler(request, exc: UserNotFound):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=str(exc),
    )


async def username_exists_handler(request, exc: UsernameAlreadyExists):
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=str(exc),
    )
