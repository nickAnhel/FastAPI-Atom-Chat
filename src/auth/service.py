from src.auth.repository import RefreshTokenRepository
from src.auth.utils import decode_jwt


class RefreshTokenService:
    def __init__(self, repository: RefreshTokenRepository) -> None:
        self._repository = repository

    async def blacklist(
        self,
        refresh_token: str,
    ) -> None:
        token = decode_jwt(token=refresh_token)
        await self._repository.create(data={"token_id": token.get("sub")})

    async def is_blacklisted(
        self,
        refresh_token: str,
    ) -> bool:
        token = decode_jwt(token=refresh_token)
        if await self._repository.get_single(token_id=token.get("sub")):
            return True

        return False
