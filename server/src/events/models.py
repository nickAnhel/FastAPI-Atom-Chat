import uuid
import datetime
from functools import partial
from sqlalchemy import ForeignKey, func, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base


class EventModel(Base):
    __tablename__ = "events"

    event_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    event_type: Mapped[str]
    created_at: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=partial(datetime.datetime.now, tz=datetime.timezone.utc),
        server_default=func.now()
    )

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"))
    user: Mapped["UserModel"] = relationship(back_populates="events")

    chat_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("chats.chat_id", ondelete="CASCADE"))
    chat: Mapped["ChatModel"] = relationship(back_populates="events")
