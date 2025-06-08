from sqlalchemy import Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from .base import Base
import uuid

class TrialNotification(Base):
    __tablename__ = "trial_notifications"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    subscription_id: Mapped[int] = mapped_column(ForeignKey("subscriptions.id"))
    notify_at: Mapped[datetime] = mapped_column(DateTime)
    is_sent: Mapped[bool] = mapped_column(Boolean, default=False)
    sent_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    # user = relationship("User", back_populates="trial_notifications")
    # subscription = relationship("Subscription", back_populates="trial_notifications")