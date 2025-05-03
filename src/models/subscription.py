from sqlalchemy import Column, Numeric, String, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID, uuid4
from datetime import datetime
from decimal import Decimal

# from src.models.expenses import Expense
# from src.models.users import User

from .base import Base  # Базовый класс моделей

import uuid

class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str] = mapped_column(String(255))
    category: Mapped[str] = mapped_column(String(100))
    price: Mapped[float] = mapped_column()
    currency: Mapped[str] = mapped_column(String(8))
    billing_period: Mapped[str] = mapped_column(String(50))
    next_payment: Mapped[datetime] = mapped_column(DateTime)
    trial_ends_at: Mapped[datetime] = mapped_column(DateTime)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_renew: Mapped[bool] = mapped_column(Boolean, default=True)
    notes: Mapped[str] = mapped_column(String(512))
    logo_url: Mapped[str] = mapped_column(String(512))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="subscriptions")
    expenses = relationship("Expense", back_populates="subscription", cascade="all, delete-orphan")
    payment_history = relationship("PaymentHistory", back_populates="subscription", cascade="all, delete-orphan")
    trial_notifications = relationship("TrialNotification", back_populates="subscription", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="subscription", cascade="all, delete-orphan")
