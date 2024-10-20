import uuid
from sqlalchemy.exc import IntegrityError, NoResultFound

from src.users.exceptions import UsernameAlreadyExists, UserNotFound
from src.users.repository import UserRepository
from src.users.schemas import UserCreate, UserGet, UserUpdate
from src.users.utils import get_password_hash
from src.users.enums import UsersOrder


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self._repository: UserRepository = repository

    async def create_user(
        self,
        data: UserCreate,
    ) -> UserGet:
        user_data = data.model_dump()
        user_data["hashed_password"] = get_password_hash(user_data["password"])
        del user_data["password"]

        try:
            user = await self._repository.create(data=user_data)
            return UserGet.model_validate(user)
        except IntegrityError as exc:
            raise UsernameAlreadyExists(f"Username {data.username!r} already exists") from exc

    async def get_user_by_id(self, user_id: uuid.UUID) -> UserGet:
        try:
            user = await self._repository.get_single(user_id=user_id)
            return UserGet.model_validate(user)
        except NoResultFound as exc:
            raise UserNotFound(f"User with id '{user_id}' not found") from exc

    async def get_users(
        self,
        order: str = UsersOrder.ID,
        desc: bool = False,
        offset: int = 0,
        limit: int = 100,
    ) -> list[UserGet]:
        users = await self._repository.get_multi(
            order=order,
            order_desc=desc,
            offset=offset,
            limit=limit,
        )
        return [UserGet.model_validate(user) for user in users]

    async def update_user(
        self,
        user_id: uuid.UUID,
        data: UserUpdate,
    ) -> UserGet:
        try:
            user = await self._repository.update(data=data.model_dump(), user_id=user_id)
            return UserGet.model_validate(user)

        except NoResultFound as exc:
            raise UserNotFound(f"User with id '{user_id}' not found") from exc

        except IntegrityError as exc:
            raise UsernameAlreadyExists(f"Username {data.username!r} already exists") from exc

    async def delete_user(
        self,
        user_id: uuid.UUID,
    ) -> bool:
        if await self._repository.delete(user_id=user_id) == 0:
            raise UserNotFound(f"User with id '{user_id}' not found")

        return True
