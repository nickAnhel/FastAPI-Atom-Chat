import uuid
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base


class ChatModel(Base):
    __tablename__ = "chats"

    chat_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    title: Mapped[str]
    is_private: Mapped[bool] = mapped_column(default=False)

    messages: Mapped[list["MessageModel"]] = relationship(back_populates="chat")
    events: Mapped[list["EventModel"]] = relationship(back_populates="chat")

    owner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"))
    owner: Mapped["UserModel"] = relationship(back_populates="created_chats")

    members: Mapped[list["UserModel"]] = relationship(
        back_populates="joined_chats",
        secondary="chat_user",
    )


class ChatUserM2M(Base):
    __tablename__ = "chat_user"

    chat_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("chats.chat_id", ondelete="CASCADE"),
        primary_key=True,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.user_id", ondelete="CASCADE"),
        primary_key=True,
    )
