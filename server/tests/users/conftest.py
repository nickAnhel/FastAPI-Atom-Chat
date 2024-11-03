import uuid
import pytest
from httpx import AsyncClient


@pytest.fixture
async def user(async_client: AsyncClient):
    user_response = await async_client.post(
        "/users/",
        json={"username": str(uuid.uuid4().hex), "password": "string12"},
    )
    user = user_response.json()

    token_response = await async_client.post(
        "/auth/login",
        data={"username": user["username"], "password": "string12"},
    )

    user.update(token_response.json())
    return user
