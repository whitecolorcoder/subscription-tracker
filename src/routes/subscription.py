from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from pydantic import BaseModel, Field, HttpUrl

from src.redis_repository.redis_repo import STORAGE_CACHE_TIME
from src.services.jwt_token_services import JWTService
from src.config import settings

from .deps import JWTServiceDep, SubscriptionRepoDep, RedisCacheDep

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

class SubscriptionOverview(SubscriptionResponceModel):
    sum_expenses: float
    
    class Config:
        from_attributes = True
        
        
class SubscritptionsOverviewList(BaseModel):
    subscriptions: list[SubscriptionOverview]

class SubscriptionFilters(BaseModel):
    categories: Optional[list[str]] = Field(None, example=["entertainment", "finance", "joke", "other"])
    is_active: Optional[bool] = Field(None, example=True)
    min_price: Optional[float] = Field(None, ge=0, example=5.0)
    max_price: Optional[float] = Field(None, ge=0, example=20.0)

@router.get("/", response_model=list[SubscriptionResponceModel])
def get_user_subscriptions(
    repo: SubscriptionRepoDep,
    token: HTTPBearer = Depends(HTTPBearer()),
    filters: SubscriptionFilters = Depends()
):
    user_id = JWTService(settings).check_jwt(token.credentials)
    return repo.get_filtered_subscriptions_sync(user_id, filters.dict(exclude_none=True))

class SubscriptionPatch(BaseModel):
    subscription_id: int
    subscription_name: Optional[str] = None
    price: Optional[float] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    auto_renewal: Optional[bool] = False

class SubscriptionCreateRequest(BaseModel):
    name: str = Field(..., max_length=255)
    category: str = Field(..., max_length=100)
    price: float = Field(..., gt=0)
    currency: str = Field(default="USD", max_length=8)
    billing_period: str = Field(default="monthly", max_length=50)
    next_payment: datetime
    trial_ends_at: datetime
    is_active: bool = Field(default=True)
    auto_renew: bool = Field(default=True)
    notes: str = Field(default="", max_length=512)
    logo_url: str = Field(None, max_length=512)

class SubscriptionResponse(BaseModel):
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
    logo_url: Optional[HttpUrl]
    created_at: datetime
     

@router.post("/", response_model=SubscriptionResponceModel, status_code=201)
def post_new_subscription(
    body: SubscriptionCreateRequest,
    repository: SubscriptionRepoDep,
    token: str = Depends(HTTPBearer()),
):
    user_id = JWTService(settings).check_jwt(token.credentials)
    db_val = repository.create_subscription(
        user_id=user_id,
        subscription_data=body
    )
    return db_val

@router.get("/{subscription_id}",  response_model=SubscriptionResponceModel, status_code=200)
def get_subscription(
    subscription_id: int,
    repository: SubscriptionRepoDep,
    token_service: JWTServiceDep,
    token: str = Depends(HTTPBearer()),
):    
    return repository.get_one_subscription(user_id=token_service.check_jwt(token.credentials), subscription_id=subscription_id)

@router.patch("/{id}", response_model=SubscriptionResponceModel, status_code=200)
def patch_subscription(
    id: int,
    body: SubscriptionPatch,
    repository: SubscriptionRepoDep,
    token_service: JWTServiceDep,
    token: str = Depends(HTTPBearer()),
):
    user_id = token_service.check_jwt(token.credentials)
        
    result = repository.update_subscription(
    user_id=user_id,
    **body.dict(exclude_none=True)
    )
    return result

@router.delete('/{subscription_id}', response_model=SubscriptionResponceModel, status_code=200)
def del_subscription(subscription_id: int,
    repository: SubscriptionRepoDep,
    token_service: JWTServiceDep,
    token: str = Depends(HTTPBearer())):

# вынести логику 'token_service.check_jwt(token.credentials' в миддлвейр либо иньекции через метод колл
    return repository.delete_subscription(user_id=token_service.check_jwt(token.credentials), 
                                          subscription_id=subscription_id)

# post/put/patch/delete. Организовать идемпотентность данных методов, через middlewere. Данные храним в кеше. 
# Токены и резельтаты успешных оперраций. Токены создает клиент, сделать проверку на валидацию. Почитать стратегии идемпотентности.
# Вывести индемпотентность из первых принципов REST арихитектуры.

# Протестировать наш миддлевере. Посмотреть нужен ли нам иденпосиди кий на ручках в теле 
