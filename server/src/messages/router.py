import uuid
from fastapi import APIRouter, Depends

from src.users.schemas import UserGet
from src.auth.dependencies import get_current_active_user

from src.messages.dependencies import get_message_service
from src.messages.service import MessageService
from src.messages.schemas import MessageGetWithUser
from src.messages.enums import MessagesOrder


router = APIRouter(
    prefix="/messages",
    tags=["Messages"],
)


@router.get("/{chat_id}")
async def get_chat(
    chat_id: uuid.UUID,
    order: MessagesOrder = MessagesOrder.CREATED_AT,
    offset: int = 0,
    limit: int = 100,
    user: UserGet = Depends(get_current_active_user),
    service: MessageService = Depends(get_message_service),
) -> list[MessageGetWithUser]:
    return await service.get_messages(
        chat_id=chat_id,
        order=order,
        order_desc=True,
        offset=offset,
        limit=limit,
    )
