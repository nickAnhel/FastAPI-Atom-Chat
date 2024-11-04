import uuid
from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, Depends, status

from src.schemas import Success
from src.users.schemas import UserGet
from src.auth.dependencies import get_current_active_user
from src.events.service import EventService
from src.events.dependencies import get_event_service
from src.events.schemas import EventCreate
from src.events.enums import EventType

from src.chats.service import ChatService
from src.chats.dependencies import get_chat_service
from src.chats.enums import ChatOrder
from src.chats.schemas import (
    ChatCreate,
    ChatGet,
    ChatUpdate,
    MessageHistoryItem,
    EventHistoryItem,
)


router = APIRouter(
    prefix="/chats",
    tags=["Chats"],
)


@router.post("/")
async def create_chat(
    data: ChatCreate,
    user: UserGet = Depends(get_current_active_user),
    chat_service: ChatService = Depends(get_chat_service),
    event_service: EventService = Depends(get_event_service),
) -> ChatGet:
    chat = await chat_service.create_chat(
        user_id=user.user_id,
        data=data,
    )

    await event_service.create_event(
        data=EventCreate(
            chat_id=chat.chat_id,
            event_type=EventType.CREATE,
            user_id=user.user_id,
        )
    )

    return chat


@router.get("/")
async def get_chats(
    order: ChatOrder = ChatOrder.ID,
    order_desc: bool = False,
    offset: int = 0,
    limit: int = 100,
    user: UserGet = Depends(get_current_active_user),
    service: ChatService = Depends(get_chat_service),
) -> list[ChatGet]:
    return await service.get_chats(
        order=order,
        order_desc=order_desc,
        offset=offset,
        limit=limit,
    )


@router.get("/search")
async def search_chats(
    query: str,
    offset: int = 0,
    limit: int = 100,
    user: UserGet = Depends(get_current_active_user),
    service: ChatService = Depends(get_chat_service),
) -> list[ChatGet]:
    return await service.search_chats(
        user_id=user.user_id,
        query=query,
        offset=offset,
        limit=limit,
    )


@router.get("/{chat_id}")
async def get_chat(
    chat_id: uuid.UUID,
    user: UserGet = Depends(get_current_active_user),
    service: ChatService = Depends(get_chat_service),
) -> ChatGet:
    return await service.get_chat(chat_id=chat_id)


@router.get("/{chat_id}/members")
async def get_chat_members(
    chat_id: uuid.UUID,
    user: UserGet = Depends(get_current_active_user),
    service: ChatService = Depends(get_chat_service),
) -> list[UserGet]:
    return await service.get_chat_members(chat_id=chat_id)


@router.get("/{chat_id}/history")
async def get_chat_history(
    chat_id: uuid.UUID,
    offset: int = 0,
    limit: int = 100,
    user: UserGet = Depends(get_current_active_user),
    service: ChatService = Depends(get_chat_service),
) -> list[MessageHistoryItem | EventHistoryItem]:
    return await service.get_chat_history(
        chat_id=chat_id,
        offset=offset,
        limit=limit,
    )


@router.post("/{chat_id}/join", status_code=status.HTTP_201_CREATED)
async def join_chat(
    chat_id: uuid.UUID,
    user: UserGet = Depends(get_current_active_user),
    chat_service: ChatService = Depends(get_chat_service),
    event_service: EventService = Depends(get_event_service),
) -> Success:
    await chat_service.join_chat(
        chat_id=chat_id,
        user=user,
    )

    await event_service.create_event(
        data=EventCreate(
            chat_id=chat_id,
            event_type=EventType.JOIN,
            user_id=user.user_id,
        )
    )

    return Success(detail="Successfully joined chat")


@router.delete("/{chat_id}/leave")
async def leave_chat(
    chat_id: uuid.UUID,
    user: UserGet = Depends(get_current_active_user),
    chat_service: ChatService = Depends(get_chat_service),
    event_service: EventService = Depends(get_event_service),
) -> Success:
    await chat_service.leave_chat(
        user_id=user.user_id,
        chat_id=chat_id,
    )

    try:
        await event_service.create_event(
            data=EventCreate(
                chat_id=chat_id,
                event_type=EventType.LEAVE,
                user_id=user.user_id,
            )
        )
    except IntegrityError:
        pass

    return Success(detail="Successfully left chat")


@router.post("/{chat_id}/add-members", status_code=status.HTTP_201_CREATED)
async def add_members_to_chat(
    chat_id: uuid.UUID,
    members_ids: list[uuid.UUID],
    user: UserGet = Depends(get_current_active_user),
    chat_service: ChatService = Depends(get_chat_service),
    event_service: EventService = Depends(get_event_service),
) -> Success:
    added_users_count = await chat_service.add_members_to_chat(
        user_id=user.user_id,
        chat_id=chat_id,
        members_ids=members_ids,
    )

    for altered_user_id in members_ids:
        await event_service.create_event(
            data=EventCreate(
                chat_id=chat_id,
                event_type=EventType.ADD,
                user_id=user.user_id,
                altered_user_id=altered_user_id,
            )
        )

    return Success(detail=f"Successfully added {added_users_count} members")


@router.delete("/{chat_id}/remove-members")
async def remove_members_from_chat(
    chat_id: uuid.UUID,
    members_ids: list[uuid.UUID],
    user: UserGet = Depends(get_current_active_user),
    chat_service: ChatService = Depends(get_chat_service),
    event_service: EventService = Depends(get_event_service),
) -> Success:
    removed_users_count = await chat_service.remove_members_from_chat(
        user_id=user.user_id,
        chat_id=chat_id,
        members_ids=members_ids,
    )

    for altered_user_id in members_ids:
        await event_service.create_event(
            data=EventCreate(
                chat_id=chat_id,
                event_type=EventType.REMOVE,
                user_id=user.user_id,
                altered_user_id=altered_user_id,
            )
        )

    return Success(detail=f"Successfully removed {removed_users_count} members")


@router.patch("/{chat_id}")
async def update_chat(
    chat_id: uuid.UUID,
    data: ChatUpdate,
    user: UserGet = Depends(get_current_active_user),
    service: ChatService = Depends(get_chat_service),
) -> ChatGet:
    return await service.update_chat(
        data=data,
        user_id=user.user_id,
        chat_id=chat_id,
    )


@router.delete("/{chat_id}")
async def delete_chat(
    chat_id: uuid.UUID,
    user: UserGet = Depends(get_current_active_user),
    service: ChatService = Depends(get_chat_service),
) -> Success:
    await service.delete_chat(
        user_id=user.user_id,
        chat_id=chat_id,
    )

    return Success(detail="Successfully deleted chat")
