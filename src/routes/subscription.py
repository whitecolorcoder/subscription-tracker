from datetime import datetime

from fastapi import APIRouter
from fastapi.security import HTTPBearer
from pydantic import BaseModel, Field, HttpUrl

from src.routes.auth import TokenBodyRequest
from src.services.jwt_token_services import JWTService

from .deps import JWTServiceDep, SubscriptionRepoDep

router = APIRouter(prefix="/subscription")


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


# @router.get("/", response_model=SubscriptionModel)
# def register_subscription(id: int, subscription_repo: SubscriptionRepoDep):
#     return SubscriptionModel(**subscription_repo.list_subscription_users(id))


@router.get("/", response_model=list[SubscriptionResponceModel], status_code=201)
def get_user_subscriptions(repo: SubscriptionRepoDep, jwt_services: JWTServiceDep, body: TokenBodyRequest):
    return repo.get_subscriptions_by_user(jwt_services.check_jwt(body.jwt_token)[1])


class SubscriptionCreate(BaseModel):
    subsription_name: str
    price: float
    start_date: datetime
    end_date: datetime
    auto_renewal: bool = False


class SubscriptionBase(BaseModel):
    user_id: int
    name: str = Field(max_length=255)
    category: str = Field(max_length=100)
    price: float
    currency: str = Field(max_length=8)
    billing_period: str = Field(max_length=50)
    next_payment: datetime
    trial_ends_at: datetime
    is_active: bool = True
    auto_renew: bool = True
    notes: str | None = Field(default=None, max_length=512)
    logo_url: HttpUrl | None = Field(default=None)


@router.post("/", response_model=SubscriptionBase, status_code=201)
def post_new_subscription(
    body: SubscriptionCreate, jwt_service: JWTService, token: HTTPBearer, repository: SubscriptionRepoDep
):
    return repository.create_subscription(user_id=jwt_service.check_jwt(token), subscription_data=body)
