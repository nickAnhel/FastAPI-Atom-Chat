import uuid
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends

from src.auth.dependencies import get_current_user_ws
from src.users.schemas import UserGet


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, *, except_for: WebSocket | None = None):
        for connection in [ws for ws in self.active_connections if ws != except_for]:
            await connection.send_text(message)


# manager = ConnectionManager()
managers: dict[int, ConnectionManager] = {}


@router.websocket("/ws/{chat_id}/{user_id}")
async def chat(
    websocket: WebSocket,
    chat_id: int,
    user_id: uuid.UUID,
    # user: UserGet = Depends(get_current_user_ws),
) -> None:
    manager: ConnectionManager = managers.get(chat_id, ConnectionManager())
    managers[chat_id] = manager

    print(managers)

    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"{user_id}: {data}", except_for=websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
