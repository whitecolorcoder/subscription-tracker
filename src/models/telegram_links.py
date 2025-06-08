from sqlalchemy import Boolean, BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
import uuid

class TelegramLink(Base):
    __tablename__ = "telegram_links"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger)
    confirmed: Mapped[bool] = mapped_column(Boolean, default=False)

    # user = relationship("User", back_populates="telegram_link")
