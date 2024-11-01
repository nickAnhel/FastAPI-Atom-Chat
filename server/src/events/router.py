import uuid
from fastapi import APIRouter, Depends

from src.auth.dependencies import get_current_active_user
from src.users.schemas import UserGet

from src.events.schemas import EventGetWithUsers
from src.events.dependencies import get_event_service
from src.events.service import EventService


router = APIRouter(
    prefix="/events",
    tags=["Events"],
)


@router.get("/")
async def get_events(
    chat_id: uuid.UUID,
    offset: int = 0,
    limit: int = 100,
    user: UserGet = Depends(get_current_active_user),
    service: EventService = Depends(get_event_service),
) -> list[EventGetWithUsers]:
    return await service.get_events(
        chat_id=chat_id,
        offset=offset,
        limit=limit,
    )
