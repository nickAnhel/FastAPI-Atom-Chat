import uuid
from fastapi import APIRouter, Depends, status

from src.schemas import Success
from src.chats.schemas import ChatGet
from src.auth.dependencies import get_current_active_user, get_current_admin_user, authenticate_user_for_restore

from src.users.service import UserService
from src.users.dependencies import get_users_service
from src.users.schemas import UserCreate, UserGet, UserUpdate
from src.users.enums import UsersOrder


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
    data: UserCreate,
    service: UserService = Depends(get_users_service),
) -> UserGet:
    return await service.create_user(data)


@router.get("/")
async def get_user_by_id(
    user_id: uuid.UUID,
    user: UserGet = Depends(get_current_active_user),
    service: UserService = Depends(get_users_service),
) -> UserGet:
    return await service.get_user_by_id(user_id)


@router.get("/me")
async def get_current_user_info(
    user: UserGet = Depends(get_current_active_user),
) -> UserGet:
    return user


@router.get("/chats")
async def get_joined_chats(
    user: UserGet = Depends(get_current_active_user),
    service: UserService = Depends(get_users_service),
) -> list[ChatGet]:
    return await service.get_joined_chats(user_id=user.user_id)


@router.get("/list")
async def get_users(
    order: UsersOrder = UsersOrder.ID,
    desc: bool = False,
    offset: int = 0,
    limit: int = 100,
    user: UserGet = Depends(get_current_active_user),
    service: UserService = Depends(get_users_service),
) -> list[UserGet]:
    return await service.get_users(
        order=order,
        desc=desc,
        offset=offset,
        limit=limit,
    )


@router.get("/search")
async def search_users(
    query: str,
    offset: int = 0,
    limit: int = 100,
    user: UserGet = Depends(get_current_active_user),
    service: UserService = Depends(get_users_service),
) -> list[UserGet]:
    return await service.search_users(
        query=query,
        user_id=user.user_id,
        offset=offset,
        limit=limit,
    )


@router.put("/")
async def update_user(
    data: UserUpdate,
    user: UserGet = Depends(get_current_active_user),
    service: UserService = Depends(get_users_service),
) -> UserGet:
    return await service.update_user(
        user_id=user.user_id,
        data=data,
    )


@router.patch("/")
async def delete_user(
    user: UserGet = Depends(get_current_active_user),
    service: UserService = Depends(get_users_service),
) -> UserGet:
    return await service.delete_user(user_id=user.user_id)


@router.patch("/restore")
async def restore_user(
    user: UserGet = Depends(authenticate_user_for_restore),
    service: UserService = Depends(get_users_service),
) -> Success:
    await service.restore_user(user_id=user.user_id)
    return Success(detail="Successfully restored user")


@router.patch("/block")
async def block_user(
    user_id: uuid.UUID,
    admin: UserGet = Depends(get_current_admin_user),
    service: UserService = Depends(get_users_service),
) -> UserGet:
    return await service.block_user(user_id=user_id)


@router.patch("/unblock")
async def unblock_user(
    user_id: uuid.UUID,
    admin: UserGet = Depends(get_current_admin_user),
    service: UserService = Depends(get_users_service),
) -> UserGet:
    return await service.unblock_user(user_id=user_id)
