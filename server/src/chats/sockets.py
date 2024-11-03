from typing import Any
import socketio

from src.database import async_session_maker
from src.messages.dependencies import get_message_service
from src.messages.schemas import MessageCreate, MessageCreateWS, MessageGetWS


sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins=[
        "http://localhost/",
        "http://localhost:5000",
    ],
)

socket_app = socketio.ASGIApp(
    socketio_server=sio,
    socketio_path="/ws",
)


@sio.on("join")
async def on_join(
    sid: str,
    data: dict[str, Any],
):
    await sio.enter_room(sid, data["chat_id"])


@sio.on("leave")
async def on_leave(
    sid: str,
    data: dict[str, Any],
):
    await sio.leave_room(sid, data["chat_id"])


@sio.on("message")
async def on_message(
    sid: str,
    data: dict[str, Any],
):
    async with async_session_maker() as session:
        service = get_message_service(session)
        msg = MessageCreateWS.model_validate(data)
        message = await service.create_message(
            MessageCreate(
                chat_id=data["chat_id"],
                user_id=data["user_id"],
                content=msg.content,
                created_at=msg.created_at.replace(tzinfo=None),
            )
        )

    await sio.emit(
        "message",
        MessageGetWS(
            message_id=message.message_id,
            username=message.user.username,
            user_id=message.user_id,
            content=message.content,
            created_at=message.created_at,
        ).model_dump_json(),
        room=data["chat_id"],
        skip_sid=sid,
    )
