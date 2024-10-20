import uuid
import pytest
from httpx import AsyncClient


@pytest.fixture
async def user(async_client: AsyncClient):
    response = await async_client.post(
        "/users/",
        json={
            "username": str(uuid.uuid4().hex),
            "password": "test",
        },
    )
    return response.json()
