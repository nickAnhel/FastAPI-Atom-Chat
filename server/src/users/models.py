import uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base


class UserModel(Base):
    __tablename__ = "users"

    user_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    is_deleted: Mapped[bool] = mapped_column(default=False)
    is_blocked: Mapped[bool] = mapped_column(default=False)
    is_admin: Mapped[bool] = mapped_column(default=False)

    messages: Mapped[list["MessageModel"]] = relationship(back_populates="user")
    created_chats: Mapped[list["ChatModel"]] = relationship(
        back_populates="owner",
    )

    joined_chats: Mapped[list["ChatModel"]] = relationship(
        back_populates="members",
        secondary="chat_user",
    )

    events: Mapped[list["EventModel"]] = relationship(back_populates="user", foreign_keys="EventModel.user_id")
    altered_events: Mapped[list["EventModel"]] = relationship(back_populates="altered_user", foreign_keys="EventModel.altered_user_id")
