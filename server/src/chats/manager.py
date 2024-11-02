import uuid
from collections import defaultdict
from fastapi import WebSocket

from src.messages.schemas import MessageGetWS


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: MessageGetWS, *, except_for: WebSocket | None = None):
        for connection in self.active_connections:
            if connection == except_for:
                continue
            await connection.send_json(message.model_dump_json())


class RoomsManager:
    def __init__(self):
        self._connection_managers: dict[uuid.UUID, ConnectionManager] = defaultdict(ConnectionManager)

    async def connect(
        self,
        chat_id: uuid.UUID,
        websocket: WebSocket,
    ) -> None:
        manager = self._connection_managers[chat_id]
        await manager.connect(websocket)

    def disconnect(
        self,
        chat_id: uuid.UUID,
        websocket: WebSocket,
    ) -> None:
        manager = self._connection_managers[chat_id]
        manager.disconnect(websocket)

        if not manager.active_connections:
            del self._connection_managers[chat_id]

        print(self._connection_managers)

    async def broadcast(
        self,
        chat_id: uuid.UUID,
        message: MessageGetWS,
        *,
        except_for: WebSocket | None = None,
    ) -> None:
        manager = self._connection_managers[chat_id]
        await manager.broadcast(message, except_for=except_for)
