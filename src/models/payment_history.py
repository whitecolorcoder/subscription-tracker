from sqlalchemy import String, DateTime, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from .base import Base
import uuid

class PaymentHistory(Base):
    __tablename__ = "payment_history"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    subscription_id: Mapped[int] = mapped_column(ForeignKey("subscriptions.id"), nullable=True)
    amount: Mapped[float] = mapped_column()
    currency: Mapped[str] = mapped_column(String(8))
    status: Mapped[str] = mapped_column(String(16))
    payment_date: Mapped[datetime] = mapped_column(DateTime)
    gateway: Mapped[str] = mapped_column(String(32))
    receipt_url: Mapped[str] = mapped_column(String(512))

    user = relationship("User", back_populates="payment_history")
    subscription = relationship("Subscription", back_populates="payment_history")
    notifications = relationship("Notification", back_populates="payment")