import uuid
import datetime

from src.schemas import BaseSchema
from src.users.schemas import UserGet
from src.events.enums import EventType


class EventCreate(BaseSchema):
    chat_id: uuid.UUID
    user_id: uuid.UUID
    event_type: EventType
    altered_user_id: uuid.UUID | None = None


class EventGet(EventCreate):
    event_id: uuid.UUID
    created_at: datetime.datetime


class EventGetWithUsers(EventGet):
    user: UserGet
    altered_user: UserGet | None
