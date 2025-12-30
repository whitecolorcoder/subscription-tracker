from datetime import datetime
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from src import repository
from src.routes.deps import JWTServiceDep, ServiceAnalyticsDep, SubscriptionRepoDep
from src.routes.expenses import BaseExpense
from src.routes.shemas import TotalOverview
from src.routes.subscription import SubscriptionOverview, SubscriptionResponceModel

router = APIRouter()

@router.get('/', response_model=list[SubscriptionOverview])
def overview_expenses(
    analitic_service: ServiceAnalyticsDep,
    token_service: JWTServiceDep,
    token: str = Depends(HTTPBearer())
):
    result = analitic_service.get_user_analytics(token_service.check_jwt(token.credentials))
    
    return [SubscriptionOverview.from_orm(subscription[0]) for subscription in result]


