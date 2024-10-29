import uuid
from sqlalchemy.exc import IntegrityError, NoResultFound

from src.chats.schemas import ChatGet
from src.users.exceptions import UsernameAlreadyExists, UserNotFound
from src.users.repository import UserRepository
from src.users.schemas import UserCreate, UserGet, UserGetWithPassword, UserUpdate
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

    async def _get_user(
        self,
        include_password: bool,
        exclude_deleted: bool,
        exclude_blocked: bool,
        **filters,
    ) -> UserGet | UserGetWithPassword:
        try:
            if exclude_blocked:
                filters["is_blocked"] = False

            if exclude_deleted:
                filters["is_deleted"] = False

            user = await self._repository.get_single(**filters)
        except NoResultFound as exc:
            raise UserNotFound(
                f"User with credentials {", ".join(f"{key}='{value!s}'" for key, value in filters.items())} not found"
            ) from exc

        if include_password:
            return UserGetWithPassword.model_validate(user)

        return UserGet.model_validate(user)

    async def get_user_by_username(
        self,
        username: str,
        include_password: bool = False,
        exclude_deleted: bool = True,
        exclude_blocked: bool = True,
    ) -> UserGet | UserGetWithPassword:
        return await self._get_user(
            include_password=include_password,
            exclude_deleted=exclude_deleted,
            exclude_blocked=exclude_blocked,
            username=username,
        )

    async def get_user_by_id(
        self,
        user_id: uuid.UUID,
        include_password: bool = False,
        exclude_deleted: bool = True,
        exclude_blocked: bool = True,
    ) -> UserGet | UserGetWithPassword:
        return await self._get_user(
            include_password=include_password,
            exclude_deleted=exclude_deleted,
            exclude_blocked=exclude_blocked,
            user_id=user_id,
        )

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

    async def search_users(
        self,
        query: str,
        user_id: uuid.UUID,
        order: str = UsersOrder.ID,
        order_desc: bool = False,
        offset: int = 0,
        limit: int = 100,
    ) -> list[UserGet]:
        users = await self._repository.search(
            q=query,
            user_id=user_id,
            order=order,
            order_desc=order_desc,
            offset=offset,
            limit=limit,
        )
        return [UserGet.model_validate(user) for user in users]

    async def get_joined_chats(
        self,
        user_id: uuid.UUID,
    ) -> list[ChatGet]:
        chats =  await self._repository.get_joined_chats(user_id=user_id)
        return [ChatGet.model_validate(chat) for chat in chats]

    async def update_user(
        self,
        user_id: uuid.UUID,
        data: UserUpdate,
    ) -> UserGet:
        try:
            user = await self._repository.update(data=data.model_dump(exclude_none=True), user_id=user_id)
            return UserGet.model_validate(user)

        except NoResultFound as exc:
            raise UserNotFound(f"User with id '{user_id}' not found") from exc

        except IntegrityError as exc:
            raise UsernameAlreadyExists(f"Username {data.username!r} already exists") from exc

    async def delete_user(
        self,
        user_id: uuid.UUID,
    ) -> bool:
        try:
            await self._repository.mark_deleted(user_id=user_id)
        except NoResultFound as exc:
            raise UserNotFound(f"User with id '{user_id}' not found") from exc

        return True

    async def restore_user(
        self,
        user_id: uuid.UUID,
    ) -> bool:
        try:
            await self._repository.mark_restored(user_id=user_id)
        except NoResultFound as exc:
            raise UserNotFound(f"User with id '{user_id}' not found") from exc

        return True
