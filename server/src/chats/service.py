import uuid
from sqlalchemy.exc import NoResultFound, IntegrityError

from src.users.schemas import UserGet
from src.messages.models import MessageModel

from src.chats.repository import ChatRepository
from src.chats.enums import ChatOrder
from src.chats.schemas import (
    ChatCreate,
    ChatGet,
    ChatUpdate,
    MessageHistoryItem,
    EventHistoryItem,
)
from src.chats.exceptions import (
    ChatNotFound,
    PermissionDenied,
    AlreadyInChat,
    CantAddMembers,
    CantRemoveMembers,
    FailedToLeaveChat,
)


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
        chat_users = [user_id]
        if data.members:
            chat_users.extend(data.members)

        try:
            await self._repository.add_members(chat_id=chat.chat_id, users_ids=chat_users)
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

    async def get_chat_history(
        self,
        *,
        chat_id: uuid.UUID,
        offset: int,
        limit: int,
    ) -> list[MessageHistoryItem | EventHistoryItem]:
        history = await self._repository.history(
            chat_id=chat_id,
            offset=offset,
            limit=limit,
        )

        items: list[MessageHistoryItem | EventHistoryItem] = [
            (
                MessageHistoryItem.model_validate(item)
                if isinstance(item, MessageModel)
                else EventHistoryItem.model_validate(item)
            )
            for item in history
        ]

        return items

    async def join_chat(
        self,
        *,
        chat_id: uuid.UUID,
        user: UserGet,
    ) -> bool:
        try:
            if not user.is_admin:
                chat = await self._repository.get_single(chat_id=chat_id)
                if chat.is_private:
                    raise PermissionDenied(f"Chat with id '{chat_id}' is private")

            return await self._repository.add_members(chat_id=chat_id, users_ids=[user.user_id]) == 1

        except NoResultFound as exc:
            raise ChatNotFound(f"Chat with id '{chat_id}' not found") from exc

        except IntegrityError as exc:
            raise AlreadyInChat(f"User with id '{user.user_id}' already in chat") from exc

    async def leave_chat(
        self,
        *,
        chat_id: uuid.UUID,
        user_id: uuid.UUID,
    ) -> None:
        if await self._repository.remove_members(chat_id=chat_id, members_ids=[user_id]) != 1:
            raise FailedToLeaveChat(f"Failed to leave chat with id '{chat_id}'")

        # Delete chat if it has no members
        if len(await self._repository.get_members(chat_id=chat_id)) == 0:
            await self._repository.delete(chat_id=chat_id)

    async def check_chat_exists_and_user_is_owner(
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
    ) -> int:
        await self.check_chat_exists_and_user_is_owner(chat_id=chat_id, user_id=user_id)

        if user_id in members_ids:
            raise CantAddMembers("Can't add yourself to chat")

        try:
            if (
                added_users_count := await self._repository.add_members(
                    chat_id=chat_id,
                    users_ids=members_ids,
                )
            ) == 0:
                raise CantAddMembers("Failed to add members")

            return added_users_count
        except IntegrityError as exc:
            raise CantAddMembers("Can't add members") from exc

    async def remove_members_from_chat(
        self,
        *,
        chat_id: uuid.UUID,
        user_id: uuid.UUID,
        members_ids: list[uuid.UUID],
    ) -> int:
        await self.check_chat_exists_and_user_is_owner(chat_id=chat_id, user_id=user_id)

        if user_id in members_ids:
            raise CantAddMembers("Can't remove yourself from chat")

        if (
            removed_users_count := await self._repository.remove_members(
                chat_id=chat_id,
                members_ids=members_ids,
            )
        ) == 0:
            raise CantRemoveMembers("Can't remove members")

        return removed_users_count

    async def update_chat(
        self,
        *,
        data: ChatUpdate,
        chat_id: uuid.UUID,
        user_id: uuid.UUID,
    ) -> ChatGet:
        await self.check_chat_exists_and_user_is_owner(chat_id=chat_id, user_id=user_id)
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
    ) -> None:
        await self.check_chat_exists_and_user_is_owner(chat_id=chat_id, user_id=user_id)
        await self._repository.delete(chat_id=chat_id)

    async def search_chats(
        self,
        *,
        user_id: uuid.UUID,
        query: str,
        offset: int,
        limit: int,
    ) -> list[ChatGet]:
        chats = await self._repository.search(
            user_id=user_id,
            q=query,
            offset=offset,
            limit=limit,
        )
        return [ChatGet.model_validate(chat) for chat in chats]
