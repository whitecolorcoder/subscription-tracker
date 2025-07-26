from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.config import settings
from src.repository.expenses import ExpensesRepo
from src.repository.subscription import SubscriptionRepo
from src.repository.user import UserRepo
from src.services.jwt_token_services import JWTService
from src.services.password_service import PasswordsService

engine=create_engine(str(settings.SQLALCHEMY_DATABASE_URI))

def get_session() -> Session:
    session=sessionmaker(bind=engine)
    with session() as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]


def get_user_repo(session: SessionDep) -> UserRepo:
    return UserRepo(session=session)

UserRepoDep = Annotated[UserRepo, Depends(get_user_repo)]

def get_subscription_repo(session: SessionDep) -> SubscriptionRepo:
    return SubscriptionRepo(session=session)

SubscriptionRepoDep = Annotated[SubscriptionRepo, Depends(get_subscription_repo)]

def get_password_services()-> PasswordsService:
    return PasswordsService()

PasswordsServiceDep = Annotated[PasswordsService, Depends(get_password_services)]

def get_jwt_service()-> JWTService:
    return JWTService(config=settings)

JWTServiceDep = Annotated[JWTService, Depends(get_jwt_service)]

def get_expenses_repo(session:SessionDep) -> ExpensesRepo:
    return ExpensesRepo(session=session)

ExpensesRepoDep = Annotated[ExpensesRepo, Depends(get_expenses_repo)]
