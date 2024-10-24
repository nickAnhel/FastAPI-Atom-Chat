from fastapi import WebSocket

from src.chat.schemas import MessageGetWS


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

    async def broadcast(self, message: MessageGetWS, *, except_for: WebSocket | None = None):
        for connection in [ws for ws in self.active_connections if ws != except_for]:
            await connection.send_json(message.model_dump_json())
