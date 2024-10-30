import uuid
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, status

from src.schemas import Success
from src.users.schemas import UserGet
from src.auth.dependencies import get_current_active_user
from src.messages.dependencies import get_message_service
from src.messages.service import MessageService
from src.messages.schemas import MessageCreate, MessageCreateWS, MessageGetWS

from src.chats.manager import ConnectionManager
from src.chats.service import ChatService
from src.chats.dependencies import get_chat_service
from src.chats.schemas import ChatCreate, ChatGet, ChatUpdate
from src.chats.enums import ChatOrder


router = APIRouter(
    prefix="/chats",
    tags=["Chats"],
)


@router.post("/")
async def create_chat(
    data: ChatCreate,
    user: UserGet = Depends(get_current_active_user),
    service: ChatService = Depends(get_chat_service),
) -> ChatGet:
    return await service.create_chat(
        user_id=user.user_id,
        data=data,
    )


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


@router.post("/{chat_id}/join", status_code=status.HTTP_201_CREATED)
async def join_chat(
    chat_id: uuid.UUID,
    user: UserGet = Depends(get_current_active_user),
    service: ChatService = Depends(get_chat_service),
) -> Success:
    await service.join_chat(
        chat_id=chat_id,
        user=user,
    )
    return Success(detail="Successfully joined chat")


@router.delete("/{chat_id}/leave")
async def leave_chat(
    chat_id: uuid.UUID,
    user: UserGet = Depends(get_current_active_user),
    service: ChatService = Depends(get_chat_service),
) -> Success:
    await service.leave_chat(
        user_id=user.user_id,
        chat_id=chat_id,
    )

    return Success(detail="Successfully left chat")


@router.post("/{chat_id}/add-members", status_code=status.HTTP_201_CREATED)
async def add_members_to_chat(
    chat_id: uuid.UUID,
    members_ids: list[uuid.UUID],
    user: UserGet = Depends(get_current_active_user),
    service: ChatService = Depends(get_chat_service),
) -> Success:
    added_users_count = await service.add_members_to_chat(
        user_id=user.user_id,
        chat_id=chat_id,
        members_ids=members_ids,
    )

    return Success(detail=f"Successfully added {added_users_count} members")


@router.delete("/{chat_id}/remove-members")
async def remove_members_from_chat(
    chat_id: uuid.UUID,
    members_ids: list[uuid.UUID],
    user: UserGet = Depends(get_current_active_user),
    service: ChatService = Depends(get_chat_service),
) -> Success:
    removed_users_count = await service.remove_members_from_chat(
        user_id=user.user_id,
        chat_id=chat_id,
        members_ids=members_ids,
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


# WebSockets
managers: dict[uuid.UUID, ConnectionManager] = {}


@router.websocket("/{chat_id}/{user_id}")
async def chat(
    websocket: WebSocket,
    chat_id: uuid.UUID,
    user_id: uuid.UUID,
    service: MessageService = Depends(get_message_service),
) -> None:
    manager: ConnectionManager = managers.get(chat_id, ConnectionManager())
    managers[chat_id] = manager

    # print(managers)

    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()

            msg = MessageCreateWS.model_validate(data)
            message = await service.create_message(
                MessageCreate(
                    chat_id=chat_id,
                    user_id=user_id,
                    content=msg.content,
                    created_at=msg.created_at.replace(tzinfo=None),
                )
            )

            await manager.broadcast(
                MessageGetWS(
                    message_id=message.message_id,
                    username=message.user.username,
                    user_id=message.user_id,
                    content=message.content,
                    created_at=message.created_at,
                ),
                except_for=websocket,
            )
    except WebSocketDisconnect:
        manager.disconnect(websocket)
