from typing import List  # Добавьте этот импорт
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer
from pydantic import BaseModel

from src.repository.expenses import ExpensesRepo
from src.routes.deps import ExpensesRepoDep, JWTServiceDep

router = APIRouter(prefix="/expenses")

class ExpenseResponseModel(BaseModel):  # Исправлено название (было опечатка)
    id: int
    user_id: int
    subscription_id: int | None  # Сделайте nullable, если в модели может быть None
    amount: float
    currency: str
    date: datetime
    description: str
    category: str

    class Config:
        from_attributes = True  # Необходимо для работы с ORM

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
