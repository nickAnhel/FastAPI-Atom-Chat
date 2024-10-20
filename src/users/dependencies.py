from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.users.service import UserService
from src.users.repository import UserRepository


def get_users_service(session: AsyncSession = Depends(get_async_session)) -> UserService:
    return UserService(UserRepository(session))
