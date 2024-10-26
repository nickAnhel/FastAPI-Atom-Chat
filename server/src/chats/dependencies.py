from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from src.database import get_async_session
from src.chats.repository import ChatRepository
from src.chats.service import ChatService


def get_chat_service(
    session: AsyncSession = Depends(get_async_session),
) -> ChatService:
    return ChatService(ChatRepository(session))
