from uuid import UUID
from typing import Any
from jwt.exceptions import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from src.database import get_async_session
from src.users.schemas import UserGet, UserGetWithPassword
from src.users.service import UserService
from src.users.dependencies import get_users_service
from src.users.exceptions import UserNotFound
from src.auth.config import auth_settings
from src.auth.utils import validate_password, decode_jwt
from src.auth.repository import RefreshTokenRepository
from src.auth.service import RefreshTokenService


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_refresh_token_service(
    session: AsyncSession = Depends(get_async_session),
) -> RefreshTokenService:
    return RefreshTokenService(RefreshTokenRepository(session))


async def authenticate_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_service: UserService = Depends(get_users_service),
) -> UserGetWithPassword:
    try:
        user: UserGetWithPassword = await user_service.get_user_by_username(
            username=form_data.username,
            include_password=True,
        )  # type: ignore
    except UserNotFound as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        ) from exc

    if not validate_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    return user


def _get_token_payload(
    token: str,
) -> dict[str, Any]:
    try:
        return decode_jwt(token)
    except InvalidTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization token",
        ) from exc


def _get_token_from_header(
    token: str = Depends(oauth2_scheme),
) -> dict[str, Any]:
    return _get_token_payload(token)


def _get_token_from_cookie(
    request: Request,
) -> dict[str, Any]:
    token = request.cookies.get(auth_settings.refresh_token_cookie_key)
    return _get_token_payload(token)  # type: ignore


def _check_token_type(
    token_payload: dict[str, Any],
    token_type: str,
) -> None:
    if not token_payload.get("type") == token_type:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Invalid token type: {token_payload.get('type')!r}",
        )


async def get_current_user(
    payload: dict[str, Any] = Depends(_get_token_from_header),
    users_service: UserService = Depends(get_users_service),
) -> UserGet:
    _check_token_type(payload, auth_settings.access_token_type)

    try:
        return await users_service.get_user_by_id(user_id=UUID(payload.get("sub")))
    except UserNotFound as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization token",
        ) from exc


async def get_current_user_for_refresh(
    payload: dict[str, Any] = Depends(_get_token_from_cookie),
    users_service: UserService = Depends(get_users_service),
) -> UserGet:
    _check_token_type(payload, auth_settings.refresh_token_type)

    try:
        return await users_service.get_user_by_id(user_id=UUID(payload.get("user_id")))
    except UserNotFound as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization token",
        ) from exc
