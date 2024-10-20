import uuid
from fastapi import APIRouter, Depends, status

from src.auth.dependencies import get_current_user
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
    users_service: UserService = Depends(get_users_service),
) -> UserGet:
    return await users_service.create_user(data)


@router.get("/me")
async def get_current_user_info(
    user: UserGet = Depends(get_current_user),
) -> UserGet:
    return user


@router.get("/")
async def get_user_by_id(
    user_id: uuid.UUID,
    users_service: UserService = Depends(get_users_service),
) -> UserGet:
    return await users_service.get_user_by_id(user_id)


@router.get("/list")
async def get_users(
    order: UsersOrder = UsersOrder.ID,
    desc: bool = False,
    offset: int = 0,
    limit: int = 100,
    users_service: UserService = Depends(get_users_service),
) -> list[UserGet]:
    return await users_service.get_users(
        order=order,
        desc=desc,
        offset=offset,
        limit=limit,
    )


@router.put("/")
async def update_user(
    # user_id: uuid.UUID,
    data: UserUpdate,
    user: UserGet = Depends(get_current_user),
    users_service: UserService = Depends(get_users_service),
) -> UserGet:
    return await users_service.update_user(
        user_id=user.user_id,
        data=data,
    )


@router.delete("/")
async def delete_user(
    # user_id: uuid.UUID,
    user: UserGet = Depends(get_current_user),
    users_service: UserService = Depends(get_users_service),
) -> bool:
    return await users_service.delete_user(user_id=user.user_id)
