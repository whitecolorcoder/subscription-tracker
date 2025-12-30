from typing import List
from datetime import datetime
from .base import Base
from sqlalchemy import ForeignKey, String, Boolean, DateTime, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import uuid


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    subscription_budget: Mapped[float] = mapped_column(Float, default=0.0)
    currency_preference: Mapped[str] = mapped_column(String(8), default='RUB')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    subscriptions = relationship("Subscription", back_populates="user", cascade="all, delete-orphan")
    expenses = relationship("Expense", back_populates="user", cascade="all, delete-orphan")
    # payment_history = relationship("PaymentHistory", back_populates="user", cascade="all, delete-orphan")
    # trial_notifications = relationship("TrialNotification", back_populates="user", cascade="all, delete-orphan")
    # notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    # websocket_sessions = relationship("WebSocketSession", back_populates="user", cascade="all, delete-orphan")
    # telegram_link = relationship("TelegramLink", back_populates="user", cascade="all, delete-orphan", uselist=False)


    def __repr__(self) -> str:
        return f"User(id={self.id!r}, email={self.email!r})"
