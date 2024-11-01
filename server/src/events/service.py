import uuid

from src.events.repository import EventRepository
from src.events.schemas import EventCreate, EventGet, EventGetWithUsers


class EventService:
    def __init__(self, repository: EventRepository) -> None:
        self._repository = repository

    async def create_event(
        self,
        *,
        data: EventCreate,
    ) -> EventGet:
        event = await self._repository.create(data=data.model_dump())
        return EventGet.model_validate(event)

    async def get_events(
        self,
        *,
        chat_id: uuid.UUID,
        offset: int,
        limit: int,
    ) -> list[EventGetWithUsers]:
        events = await self._repository.get_multi(
            chat_id=chat_id,
            offset=offset,
            limit=limit,
        )

        return [EventGetWithUsers.model_validate(event) for event in events]
