from fastapi import Depends
from typing import Annotated

from datetime import datetime
from src.repository.subscription import SubscriptionRepo

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi import APIRouter
from src.config import settings
from src.repository.user import UserRepo
from pydantic import BaseModel, EmailStr

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
    return SubscriptionRepo(sessiom=session)

SubscriptionRepoDep = Annotated[SubscriptionRepo, Depends(get_subscription_repo)] 

def get_password_services()-> PasswordsService:
    return PasswordsService()

PasswordsServiceDep = Annotated[PasswordsService, Depends(get_password_services)]

