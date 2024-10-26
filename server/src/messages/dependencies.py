from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.messages.repository import MessageRepository
from src.messages.service import MessageService


def get_message_service(
    session: AsyncSession = Depends(get_async_session),
):
    return MessageService(
        repostory=MessageRepository(session),
    )
