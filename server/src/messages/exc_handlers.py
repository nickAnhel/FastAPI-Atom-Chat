from fastapi import HTTPException, status

from src.messages.exceptions import CantUpdateMessage, CantDeleteMessage


async def cant_update_message_handler(request, exc: CantUpdateMessage):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=str(exc),
    )


async def cant_delete_message_handler(request, exc: CantDeleteMessage):
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=str(exc),
    )
