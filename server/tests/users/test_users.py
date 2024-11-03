from typing import Any
import uuid
import pytest
from httpx import AsyncClient


# Create user tests
async def test_create_user_success(async_client: AsyncClient):
    response = await async_client.post(
        "/users/",
        json={"username": "test", "password": "string12"},
    )
    assert response.status_code == 201
    assert response.json()["username"] == "test"


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
        json={"username": username, "password": "string12"},
    )
    assert response.status_code == 422


@pytest.mark.parametrize(
    "password",
    [
        "",
        "str12",
        "a" * 8,
        "1" * 8,
        "a" * 21,
    ],
)
async def test_create_user_wrong_password(
    async_client: AsyncClient,
    password: str,
):
    response = await async_client.post(
        "/users/",
        json={"username": "test", "password": password},
    )
    assert response.status_code == 422


async def test_create_user_already_exists(async_client: AsyncClient):
    response = await async_client.post(
        "/users/",
        json={"username": "test", "password": "string12"},
    )
    assert response.status_code == 409


# Get user tests
async def test_get_user_by_id_success(
    async_client: AsyncClient,
    user: dict[str, Any],
):
    response = await async_client.get(
        "/users/",
        params={"user_id": user["user_id"]},
        headers={"Authorization": f"Bearer {user['access_token']}"},
    )
    assert response.status_code == 200
    assert response.json()["username"] == user["username"]


async def test_get_user_by_id_not_found(async_client: AsyncClient):
    response = await async_client.get(f"/users/{uuid.uuid4()}")
    assert response.status_code == 404


# Get users tests
async def test_get_users_success(
    async_client: AsyncClient,
    user: dict[str, Any],
):
    response = await async_client.get(
        "/users/list",
        headers={"Authorization": f"Bearer {user['access_token']}"},
    )
    assert response.status_code == 200
    assert len(response.json()) == 4


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


# Get users chats
async def test_get_users_chats_success(
    async_client: AsyncClient,
    user: dict[str, Any],
):
    response = await async_client.get(
        "/users/chats",
        headers={"Authorization": f"Bearer {user['access_token']}"},
    )
    assert response.status_code == 200
    assert response.json() == []


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


# Delete user tests
async def test_delete_user_success(
    async_client: AsyncClient,
    user: dict[str, Any],
):
    response = await async_client.patch(
        "/users/",
        headers={"Authorization": f"Bearer {user['access_token']}"},
    )
    assert response.status_code == 200
    assert response.json()["is_deleted"] is True


# Restore user
async def test_restore_user_success(async_client: AsyncClient):
    user_response = await async_client.post(
        "/users/",
        json={"username": "test", "password": "string12"},
    )
    token_response = await async_client.post(
        "/auth/login",
        data={"username": "test", "password": "string12"},
    )

    response = await async_client.patch(
        "/users/",
        headers={"Authorization": f"Bearer {token_response.json()['access_token']}"},
    )
    assert response.status_code == 200
    assert response.json()["is_deleted"] is True

    response = await async_client.patch(
        "/users/restore",
        data={"username": "test", "password": "string12"},
    )

    assert response.status_code == 200


# Block user
async def test_block_user_success(
    async_client: AsyncClient,
    admin_user: dict[str, Any],
):
    response = await async_client.get(
        "/users/list",
        headers={"Authorization": f"Bearer {admin_user['access_token']}"},
    )
    for user in response.json():
        if user["username"] != "admin":
            break

    assert user["username"] != "admin"

    response = await async_client.patch(
        "/users/block?user_id=" + str(user["user_id"]),
        headers={"Authorization": f"Bearer {admin_user['access_token']}"},
    )
    assert response.status_code == 200
    assert response.json()["is_blocked"] is True


# Unblock user
async def test_unblock_user_success(
    async_client: AsyncClient,
    admin_user: dict[str, Any],
):
    response = await async_client.get(
        "/users/list",
        headers={"Authorization": f"Bearer {admin_user['access_token']}"},
    )
    for user in response.json():
        if user["username"] != "admin":
            break

    assert user["username"] != "admin"

    response = await async_client.patch(
        "/users/block?user_id=" + str(user["user_id"]),
        headers={"Authorization": f"Bearer {admin_user['access_token']}"},
    )
    assert response.status_code == 200
    assert response.json()["is_blocked"] is True

    response = await async_client.patch(
        "/users/unblock?user_id=" + str(user["user_id"]),
        headers={"Authorization": f"Bearer {admin_user['access_token']}"},
    )
    assert response.status_code == 200
    assert response.json()["is_blocked"] is False
