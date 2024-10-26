from fastapi import HTTPException, status

from src.chats.exceptions import ChatNotFound, PermissionDenied, AlreadyInChat, CantAddMembers


async def chat_not_found_handler(request, exc: ChatNotFound):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=str(exc),
    )


async def permission_denied_handler(request, exc: PermissionDenied):
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=str(exc),
    )


async def already_in_chat_handler(request, exc: AlreadyInChat):
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=str(exc),
    )


async def cant_add_members_handler(request, exc: CantAddMembers):
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=str(exc),
    )
