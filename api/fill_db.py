from typing import Any
import httpx


def create_users() -> list[dict[str, Any]]:
    users = []

    for i in range(3):
        res = httpx.post(
            "http://localhost:8000/users/",
            json={"username": f"user{i + 1}", "password": "atom1234"},
        )
        user = res.json()
        users.append(user)

        print(f"Created user {user["username"]}")

    return users


def create_chats(users: list[dict[str, Any]]) -> None:
    for i in range(3):
        res = httpx.post(
            "http://localhost:8000/auth/login",
            data={
                "username": users[i]["username"],
                "password": "atom1234",
            },
        )
        token = res.json()["access_token"]
        members = [user["user_id"] for user in users if user["user_id"] != users[i]["user_id"]]

        res = httpx.post(
            "http://localhost:8000/chats/",
            json={
                "title": f"chat{i + 1}",
                "is_private": False,
                "members": members,
            },
            headers={"Authorization": f"Bearer {token}"},
        )

        chat = res.json()
        print(f"Created chat {chat["title"]} with owner {users[i]["username"]}")


def main() -> None:
    users = create_users()
    create_chats(users)


if __name__ == "__main__":
    main()
