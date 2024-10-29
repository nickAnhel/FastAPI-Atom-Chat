from fastapi import HTTPException, status

from src.messages.exceptions import CantUpdateMessage


async def cant_update_message_handler(request, exc: CantUpdateMessage):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=str(exc),
    )
