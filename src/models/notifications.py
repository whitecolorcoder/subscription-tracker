from sqlalchemy import String, DateTime, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from .base import Base
import uuid

class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    subscription_id: Mapped[int] = mapped_column(ForeignKey("subscriptions.id"), nullable=True)
    payment_id: Mapped[int] = mapped_column(ForeignKey("payment_history.id"), nullable=True)
    type: Mapped[str] = mapped_column(String(8))
    status: Mapped[str] = mapped_column(String(16))
    message: Mapped[str] = mapped_column(Text)
    sent_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    user = relationship("User", back_populates="notifications")
    subscription = relationship("Subscription", back_populates="notifications")
    payment = relationship("PaymentHistory", back_populates="notifications")
