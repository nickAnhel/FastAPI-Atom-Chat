import uuid
from sqlalchemy.exc import NoResultFound, IntegrityError

from src.users.schemas import UserGet

from src.chats.repository import ChatRepository
from src.chats.schemas import ChatCreate, ChatGet, ChatUpdate
from src.chats.enums import ChatOrder
from src.chats.exceptions import ChatNotFound, PermissionDenied, AlreadyInChat, CantAddMembers


class ChatService:
    def __init__(self, repository: ChatRepository) -> None:
        self._repository = repository

    async def create_chat(
        self,
        user_id: uuid.UUID,
        data: ChatCreate,
    ) -> ChatGet:
        chat_data = data.model_dump(exclude={"members"})
        chat_data["owner_id"] = user_id
        chat = await self._repository.create(data=chat_data)

        # Add members to chat
        chat_users = [(chat.chat_id, user_id)]
        if data.members:
            chat_users.extend(
                [(chat.chat_id, member_id) for member_id in data.members],
            )

        try:
            await self._repository.add_members(data=chat_users)
        except IntegrityError as exc:
            raise CantAddMembers("Can't add members") from exc

        return ChatGet.model_validate(chat)

    async def get_chat(
        self,
        *,
        chat_id: uuid.UUID,
    ) -> ChatGet:
        try:
            chat = await self._repository.get_single(chat_id=chat_id)
            return ChatGet.model_validate(chat)
        except NoResultFound as exc:
            raise ChatNotFound(f"Chat with id '{chat_id}' not found") from exc

    async def get_chat_members(
        self,
        *,
        chat_id: uuid.UUID,
    ) -> list[UserGet]:
        try:
            members = await self._repository.get_members(chat_id=chat_id)
            return [UserGet.model_validate(member) for member in members]
        except NoResultFound as exc:
            raise ChatNotFound(f"Chat with id '{chat_id}' not found") from exc

    async def get_chats(
        self,
        *,
        order: ChatOrder,
        order_desc: bool,
        offset: int,
        limit: int,
    ) -> list[ChatGet]:
        chats = await self._repository.get_multi(
            order=order,
            order_desc=order_desc,
            offset=offset,
            limit=limit,
        )
        return [ChatGet.model_validate(chat) for chat in chats]

    async def join_chat(
        self,
        *,
        chat_id: uuid.UUID,
        user_id: uuid.UUID,
    ) -> bool:
        try:
            chat = await self._repository.get_single(chat_id=chat_id)
            if chat.is_private:
                raise PermissionDenied(f"Chat with id '{chat_id}' is private")

            return await self._repository.add_members([(chat_id, user_id)]) == 1

        except NoResultFound as exc:
            raise ChatNotFound(f"Chat with id '{chat_id}' not found") from exc

        except IntegrityError as exc:
            raise AlreadyInChat(f"User with id '{user_id}' already in chat") from exc

    async def leave_chat(
        self,
        *,
        chat_id: uuid.UUID,
        user_id: uuid.UUID,
    ) -> bool:
        return await self._repository.remove_members(chat_id=chat_id, members_ids=[user_id]) == 1

    async def _check_chat_exists_and_user_is_owner(
        self,
        *,
        chat_id: uuid.UUID,
        user_id: uuid.UUID,
    ) -> None:
        try:
            chat = await self._repository.get_single(chat_id=chat_id)
        except NoResultFound as exc:
            raise ChatNotFound(f"Chat with id '{chat_id}' not found") from exc

        if chat.owner_id != user_id:
            raise PermissionDenied(f"User with id '{user_id}' is not owner of chat with id '{chat_id}'")

    async def add_members_to_chat(
        self,
        *,
        chat_id: uuid.UUID,
        user_id: uuid.UUID,
        members_ids: list[uuid.UUID],
    ) -> bool:
        await self._check_chat_exists_and_user_is_owner(chat_id=chat_id, user_id=user_id)
        try:
            return await self._repository.add_members(
                [(chat_id, member_id) for member_id in members_ids],
            ) == 1
        except IntegrityError as exc:
            raise CantAddMembers("Can't add members") from exc

    async def remove_members_from_chat(
        self,
        *,
        chat_id: uuid.UUID,
        user_id: uuid.UUID,
        members_ids: list[uuid.UUID],
    ) -> bool:
        await self._check_chat_exists_and_user_is_owner(chat_id=chat_id, user_id=user_id)
        return await self._repository.remove_members(
            chat_id=chat_id,
            members_ids=members_ids,
        ) == len(members_ids)

    async def update_chat(
        self,
        *,
        data: ChatUpdate,
        chat_id: uuid.UUID,
        user_id: uuid.UUID,
    ):
        await self._check_chat_exists_and_user_is_owner(chat_id=chat_id, user_id=user_id)
        chat = await self._repository.update(
            data=data.model_dump(exclude_none=True),
            chat_id=chat_id,
        )
        return ChatGet.model_validate(chat)

    async def delete_chat(
        self,
        *,
        chat_id: uuid.UUID,
        user_id: uuid.UUID,
    ) -> bool:
        await self._check_chat_exists_and_user_is_owner(chat_id=chat_id, user_id=user_id)
        return await self._repository.delete(chat_id=chat_id) == 1
