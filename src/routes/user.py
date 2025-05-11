from datetime import datetime


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import APIRouter, Form
from src.config import settings
from src.repository.user import UserRepo
from pydantic import BaseModel, EmailStr

router= APIRouter(prefix='/user')

class UserResponceModel(BaseModel):
    id: int 
    email: EmailStr
    hashed_password: str
    is_active: bool
    subscriptiondatetime: float
    currency_preference: str
    created_at: datetime

@router.get("/", response_model=UserResponceModel)
def root(id:int):
    engine=create_engine(str(settings.SQLALCHEMY_DATABASE_URI))
    session=sessionmaker(bind=engine)
    with session() as session: 
        create_UserRepo = UserRepo(session=session).back_information_from_user(id)
        return UserResponceModel(**create_UserRepo)
    
# @router.post("/")
# def register_user():
#     engine=create_engine(str(settings.SQLALCHEMY_DATABASE_URI))
#     session=sessionmaker(bind=engine)
#     with session() as session: 
#         create_UserRepo = UserRepo(session=session).register_user(password, email)
#         return UserResponceModel(**create_UserRepo)
# 