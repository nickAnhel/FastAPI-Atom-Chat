import uuid
from sqlalchemy.orm import Mapped, mapped_column

from src.models import Base


class RefreshTokenModel(Base):
    __tablename__ = "refresh_token_blacklist"

    token_id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
