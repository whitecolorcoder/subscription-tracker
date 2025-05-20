from datetime import datetime


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import APIRouter, Form
from src.config import settings
from src.repository.subscription import SubscriptionRepo
from pydantic import BaseModel

from .deps import SubscriptionRepoDep

router= APIRouter(prefix='/subscription')

class SubscriptionModel(BaseModel):
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

@router.get("/", response_model=SubscriptionModel)
def register_subscription(id: int, subscription_repo: SubscriptionRepoDep):
    return SubscriptionModel(**subscription_repo.list_subscription_users(id))

