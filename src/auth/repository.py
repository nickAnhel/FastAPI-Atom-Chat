from typing import Any
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import RefreshTokenModel


class RefreshTokenRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self,
        data: dict[str, Any],
    ) -> None:
        stmt = (
            insert(RefreshTokenModel)
            .values(**data)
        )

        await self._session.execute(stmt)
        await self._session.commit()

    async def get_single(
        self,
        **filters,
    ) -> RefreshTokenModel | None:
        query = (
            select(RefreshTokenModel)
            .filter_by(**filters)
        )
        result = await self._session.execute(query)
        return result.scalar_one_or_none()
