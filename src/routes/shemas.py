from datetime import datetime
from pydantic import BaseModel


class TokenBodyRequest(BaseModel):
    jwt_token: str


class SubscriptionResponceModel(BaseModel):
    id: int
    user_id: int
    name: str
    category: str
    price: float
    currency: str
    billing_period: str
    next_payment: datetime
    trial_ends_at: datetime
    is_active: bool
    auto_renew: bool
    notes: str
    logo_url: str
    created_at: datetime

class BaseExpense(BaseModel):  # Исправлено название (было опечатка)
    id: int
    subscription_id: int | None  # Сделайте nullable, если в модели может быть None
    amount: float
    currency: str
    date: datetime
    description: str
    category: str

class TotalOverview(BaseModel):
    expcenses: list[BaseExpense]
    subscriptions: SubscriptionResponceModel