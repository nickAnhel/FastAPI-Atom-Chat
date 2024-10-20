import uuid
from sqlalchemy.orm import Mapped, mapped_column

from src.models import Base


class UserModel(Base):
    __tablename__ = "users"

    user_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
