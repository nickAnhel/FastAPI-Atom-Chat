import uuid
from fastapi import APIRouter, Depends

from src.schemas import Success
from src.users.schemas import UserGet
from src.auth.dependencies import get_current_active_user
from src.chats.service import ChatService
from src.chats.dependencies import get_chat_service

from src.messages.dependencies import get_message_service
from src.messages.service import MessageService
from src.messages.schemas import MessageGet, MessageGetWithUser, MessageUpdate
from src.messages.enums import MessagesOrder


router = APIRouter(
    prefix="/messages",
    tags=["Messages"],
)


@router.get("/")
async def get_chat_messages(
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


@router.get("/search")
async def search_chat_messages(
    chat_id: uuid.UUID,
    query: str,
    order: MessagesOrder = MessagesOrder.CREATED_AT,
    offset: int = 0,
    limit: int = 100,
    user: UserGet = Depends(get_current_active_user),
    service: MessageService = Depends(get_message_service),
) -> list[MessageGetWithUser]:
    return await service.search_messages(
        chat_id=chat_id,
        query=query,
        order=order,
        order_desc=True,
        offset=offset,
        limit=limit,
    )


@router.delete("/")
async def clear_chat_messages(
    chat_id: uuid.UUID,
    user: UserGet = Depends(get_current_active_user),
    message_service: MessageService = Depends(get_message_service),
    chat_service: ChatService = Depends(get_chat_service),
) -> Success:
    await chat_service.check_chat_exists_and_user_is_owner(chat_id=chat_id, user_id=user.user_id)
    deleted_messages_count = await message_service.delete_messages(chat_id=chat_id)
    return Success(detail=f"Successfully deleted {deleted_messages_count} messages")


@router.delete("/{message_id}")
async def delete_message(
    message_id: uuid.UUID,
    user: UserGet = Depends(get_current_active_user),
    service: MessageService = Depends(get_message_service),
) -> Success:
    await service.delete_message(message_id=message_id, user_id=user.user_id)
    return Success(detail="Successfully deleted message")


@router.patch("/{message_id}")
async def update_message(
    message_id: uuid.UUID,
    data: MessageUpdate,
    user: UserGet = Depends(get_current_active_user),
    service: MessageService = Depends(get_message_service),
) -> MessageGet:
    return await service.udpate_message(
        data=data,
        message_id=message_id,
        user_id=user.user_id,
    )
