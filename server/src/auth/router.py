from fastapi import (
    status,
    Depends,
    APIRouter,
    HTTPException,
    Request,
    Response,
)

from src.users.schemas import UserGet, UserGetWithPassword
from src.auth.schemas import Token
from src.auth.service import RefreshTokenService
from src.auth.config import auth_settings
from src.auth.utils import create_access_token, create_refresh_token
from src.auth.dependencies import (
    authenticate_user,
    get_current_active_user_for_refresh,
    get_refresh_token_service,
)

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/login")
async def login(
    response: Response,
    user: UserGetWithPassword = Depends(authenticate_user),
) -> Token:
    access_token = create_access_token(user=user)
    refresh_token = create_refresh_token(user=user)

    response.set_cookie(
        key=auth_settings.refresh_token_cookie_key,
        value=refresh_token,
        # max_age=auth_settings.refresh_token_expire_minutes * 60,
        # expires=auth_settings.refresh_token_expire_minutes * 60,
        httponly=True,
        samesite="lax",
        secure=False,
    )

    return Token(access_token=access_token)


@router.post("/new-access-token")
async def get_new_access_token(
    user: UserGet = Depends(get_current_active_user_for_refresh),
) -> Token:
    access_token = create_access_token(user=user)
    return Token(access_token=access_token)


@router.post("/new-refresh-token")
async def get_new_refresh_token(
    request: Request,
    response: Response,
    user: UserGet = Depends(get_current_active_user_for_refresh),
    service: RefreshTokenService = Depends(get_refresh_token_service),
) -> None:
    old_refresh_token = request.cookies.get(auth_settings.refresh_token_cookie_key)

    if await service.is_blacklisted(refresh_token=old_refresh_token):  # type: ignore
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid authorization token",
        )

    await service.blacklist(refresh_token=old_refresh_token)  # type: ignore

    refresh_token = create_refresh_token(user=user)
    response.set_cookie(
        key=auth_settings.refresh_token_cookie_key,
        value=refresh_token,
        max_age=auth_settings.refresh_token_expire_minutes * 60,
        expires=auth_settings.refresh_token_expire_minutes * 60,
        httponly=True,
    )


@router.post("/logout")
async def logout(
    response: Response,
) -> None:
    response.delete_cookie(key=auth_settings.refresh_token_cookie_key)
