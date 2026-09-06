from typing import Any

from Models.Model_Session import Model_Session
from Models.Model_User import Model_User
from Utils.common import hash_password


async def find_user_by_email(email: str) -> dict[str, Any] | None:
    users = await Model_User.select(where={"email": email}, limit=1)
    return users[0] if users else None


async def find_user_by_id(user_id: int) -> dict[str, Any] | None:
    users = await Model_User.select(columns="id, username, email", where={"id": user_id}, limit=1)
    return users[0] if users else None


async def user_exists(username: str, email: str) -> bool:
    users = await Model_User.select(where={"email": email})
    return bool(users) or bool(await Model_User.select(where={"username": username}))


async def create_user(username: str, email: str, password: str) -> dict[str, Any]:
    user_id = await Model_User.insert({
        "username": username,
        "email": email,
        "password_hash": hash_password(password),
    })
    return (await Model_User.select(columns="id, username, email", where={"id": user_id}, limit=1))[0]


async def create_session(user_id: int, token: str, expires_at: str) -> None:
    await Model_Session.insert({"user_id": user_id, "token": token, "expires_at": expires_at})


async def get_session(token: str) -> dict[str, Any] | None:
    sessions = await Model_Session.select(where={"token": token}, limit=1)
    return sessions[0] if sessions else None


async def delete_session(token: str) -> int:
    return await Model_Session.delete({"token": token})
