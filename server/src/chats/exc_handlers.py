from fastapi import HTTPException, status

from src.chats.exceptions import (
    ChatNotFound,
    PermissionDenied,
    AlreadyInChat,
    CantAddMembers,
    CantRemoveMembers,
    FailedToLeaveChat,
)


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


async def failed_to_leave_chat_handler(request, exc: FailedToLeaveChat):
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=str(exc),
    )


async def cant_add_members_handler(request, exc: CantAddMembers):
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=str(exc),
    )


async def cant_remove_members_handler(request, exc: CantRemoveMembers):
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=str(exc),
    )
