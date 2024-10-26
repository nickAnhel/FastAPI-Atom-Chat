import uuid
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends

from src.auth.dependencies import get_current_active_user
from src.users.schemas import UserGet
from src.chat.dependencies import get_message_service
from src.chat.service import MessageService
from src.chat.schemas import MessageCreate, MessageGetWithUser, MessageCreateWS, MessageGetWS
from src.chat.manager import ConnectionManager
from src.chat.enums import MessageOrder


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.get("/{chat_id}/messages")
async def get_chat(
    chat_id: int,
    offset: int = 0,
    limit: int = 100,
    user: UserGet = Depends(get_current_active_user),
    service: MessageService = Depends(get_message_service),
) -> list[MessageGetWithUser]:
    return await service.get_list(
        chat_id=chat_id,
        order=MessageOrder.CREATED_AT,
        order_desc=True,
        offset=offset,
        limit=limit,
    )


managers: dict[int, ConnectionManager] = {}


@router.websocket("/ws/{chat_id}/{user_id}")
async def chat(
    websocket: WebSocket,
    chat_id: int,
    user_id: uuid.UUID,
    service: MessageService = Depends(get_message_service),
) -> None:
    manager: ConnectionManager = managers.get(chat_id, ConnectionManager())
    managers[chat_id] = manager

    print(managers)

    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()

            msg = MessageCreateWS.model_validate(data)
            message = await service.add_message(
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
                    content=msg.content,
                    created_at=msg.created_at,
                ),
                except_for=websocket,
            )
    except WebSocketDisconnect:
        manager.disconnect(websocket)
