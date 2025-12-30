from typing import Dict, List  # Добавьте этот импорт
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer
from pydantic import BaseModel

from src.models.subscription import Subscription
from src.repository.expenses import ExpensesRepo
from src.routes.deps import ExpensesRepoDep, JWTServiceDep, SubscriptionRepoDep


router = APIRouter(prefix="/expenses")


class BaseExpense(BaseModel):  # Исправлено название (было опечатка)
    id: int
    subscription_id: int | None  # Сделайте nullable, если в модели может быть None
    amount: float
    currency: str
    date: datetime
    description: str
    category: str

    class Config:
        from_attributes = True  # Необходимо для работы с ORM
        extra = "forbid"

class ExpenseResponseModel(BaseExpense):
    user_id :int

class ExpensesRequestModel(BaseExpense):
    ...

@router.get("/", response_model=List[ExpenseResponseModel])  # Убрали status_code
def get_expenses_user_list(
    repo: ExpensesRepoDep,  # Используем только одну зависимость
    token_service: JWTServiceDep,
    token: str = Depends(HTTPBearer())
):
    user_id = token_service.check_jwt(token.credentials)
    expenses = repo.get_list_expenses(user_id)
    if not expenses:
        raise HTTPException(status_code=404, detail="No expenses found")
    return expenses


@router.post("/{id_subscription}", response_model=ExpenseResponseModel, status_code=201)
def create_expense_user(id_subscription: int,
                        repo_expense: ExpensesRepoDep,
                        repo_sub:SubscriptionRepoDep,
                        token_service: JWTServiceDep,
                        token: str = Depends(HTTPBearer())):

    user_id = token_service.check_jwt(token.credentials)
    sub=repo_sub.get_one_subscription(user_id, subscription_id=id_subscription)
    return repo_expense.create(Subscription(id=sub))

# Получить сводку расходов по категориям
class CategoryExpenes(BaseModel):
    category: str

class TotalPriceByCategory(BaseModel):
    total_price: float

@router.get("/summary", response_model=TotalPriceByCategory)
def return_price_category(
    repo: SubscriptionRepoDep,
    body: CategoryExpenes,
    token_service: JWTServiceDep,
    token: str = Depends(HTTPBearer())):

    user_id = token_service.check_jwt(token.credentials)

    return repo.sum_price_by_category(body.category, user_id)

