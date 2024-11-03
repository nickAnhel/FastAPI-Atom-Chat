import typing
import pytest
from sqlalchemy import insert
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from httpx import AsyncClient, ASGITransport

from src.main import app
from src.config import settings
from src.database import get_async_session
from src.models import Base
from src.users.models import UserModel
from src.users.utils import get_password_hash


test_engine = create_async_engine(
    url=settings.database.db_url,
    poolclass=NullPool,
)

test_session_maker = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def override_get_async_session() -> typing.AsyncGenerator[AsyncSession, None]:
    async with test_session_maker() as session:
        yield session


app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(scope="session", autouse=True)
async def setup_db():
    assert settings.database.DB_MODE == "TEST"

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.execute(
            insert(UserModel).values(
                username="admin",
                hashed_password=get_password_hash("admin123"),
                is_admin=True,
            )
        )

    yield

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
async def async_client() -> typing.AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as ac:
        yield ac
