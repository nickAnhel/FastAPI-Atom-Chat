from typing import Any
import uuid
import pytest
from httpx import AsyncClient


# Create user tests
async def test_create_user_success(async_client: AsyncClient):
    response = await async_client.post(
        "/users/",
        json={"username": "test", "password": "test"},
    )
    assert response.status_code == 201
    assert response.json()["username"] == "test"


# TODO: add tests for wrong password


@pytest.mark.parametrize(
    "username",
    ["", "a" * 33],
)
async def test_create_user_wrong_username(
    async_client: AsyncClient,
    username: str,
):
    response = await async_client.post(
        "/users/",
        json={"username": username, "password": "test"},
    )
    assert response.status_code == 422


async def test_create_user_already_exists(async_client: AsyncClient):
    response = await async_client.post(
        "/users/",
        json={"username": "test", "password": "test"},
    )
    assert response.status_code == 409


# Get user tests
async def test_get_user_by_id_success(async_client: AsyncClient):
    response = await async_client.post(
        "/users/",
        json={"username": "test2", "password": "test"},
    )
    response = await async_client.get("/users/", params={"user_id": response.json()["user_id"]})
    assert response.status_code == 200
    assert response.json()["username"] == "test2"


async def test_get_user_by_id_not_found(async_client: AsyncClient):
    response = await async_client.get(f"/users/{uuid.uuid4()}")
    assert response.status_code == 404


# Get users tests
async def test_get_users_success(async_client: AsyncClient):
    response = await async_client.get("/users/list")
    assert response.status_code == 200
    assert len(response.json()) == 2


# Get current user info tests
async def test_get_current_user_info_success(
    async_client: AsyncClient,
    user: dict[str, Any],
):
    response = await async_client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {user['access_token']}"},
    )
    assert response.status_code == 200
    assert response.json()["username"] == user["username"]



# Update user tests
async def test_update_user_success(
    async_client: AsyncClient,
    user: dict[str, Any],
):
    response = await async_client.put(
        "/users/",
        json={"username": "updated"},
        headers={"Authorization": f"Bearer {user['access_token']}"},
    )
    assert response.status_code == 200
    assert response.json()["username"] == "updated"


@pytest.mark.parametrize(
    "username",
    ["", "a" * 33],
)
async def test_update_user_wrong_username(
    async_client: AsyncClient,
    username: str,
    user: dict[str, Any],
):
    response = await async_client.put(
        "/users/",
        headers={"Authorization": f"Bearer {user['access_token']}"},
        json={"username": username},
    )
    assert response.status_code == 422


# async def test_update_user_not_found(async_client: AsyncClient):
#     response = await async_client.put(
#         "/users/",
#         json={"username": "updated"},
#     )
#     assert response.status_code == 404


# Delete user tests
async def test_delete_user_success(
    async_client: AsyncClient,
    user: dict[str, Any],
):
    response = await async_client.delete(
        "/users/",
        headers={"Authorization": f"Bearer {user['access_token']}"},
    )
    assert response.status_code == 200
    assert response.json() is True


# async def test_delete_user_not_found(async_client: AsyncClient):
#     response = await async_client.delete(f"/users/{uuid.uuid4()}")
#     assert response.status_code == 404
