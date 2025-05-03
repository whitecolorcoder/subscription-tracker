
from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID, uuid4
from datetime import datetime
from decimal import Decimal

# from src.models.subscription import Subscription
# from src.models.users import User

from .base import Base  
import uuid

class Expense(Base):
    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    subscription_id: Mapped[int] = mapped_column(ForeignKey("subscriptions.id"), nullable=True)
    amount: Mapped[float] = mapped_column()
    currency: Mapped[str] = mapped_column(String(8))
    date: Mapped[datetime] = mapped_column(DateTime)
    description: Mapped[str] = mapped_column(Text)
    category: Mapped[str] = mapped_column(String(100))

    user = relationship("User", back_populates="expenses")
    subscription = relationship("Subscription", back_populates="expenses")
