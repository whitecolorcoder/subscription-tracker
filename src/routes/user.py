from datetime import datetime

from sqlalchemy.orm import sessionmaker
from fastapi import APIRouter, HTTPException
from src.config import settings
# from src.redis_repository.redis_repo import RedisUser
from src.repository.user import NoUserInDb
from pydantic import BaseModel, EmailStr
from .deps import UserRepoDep
#RedisUserDep

router= APIRouter(prefix='/user')

class UserResponceModel(BaseModel):
    id: int
    email: EmailStr
    hashed_password: str
    is_active: bool
    currency_preference: str
    created_at: datetime


@router.get("/{id}", response_model=UserResponceModel)
def root(id: int, user_repo: UserRepoDep) -> UserResponceModel:
    try:
        user = user_repo.back_information_from_user(id)
        return user
    except NoUserInDb:
        raise HTTPException(status_code=404, detail="User not found")

#TODO почитать что такое идемпотентность


#TODO добавить кеширование на роутеры, попробовать разные варианты/стратегии 
#TODO почитать про ETAG и Last-Modified
#TODO посмотреть на схемах как выглядит кеширование
#TODO Delete почитать как удалять с кешем
# "Cache-Control"
# no-cache - проверять с сервером перед использованием кеша
# no-store - не кешировать вообще
# public - может кешироваться любыми кешами
# private - только браузер может кешировать
# max-age=3600 - время жизни в секундах
# must-revalidate - проверять после истечения


# Client                    Cache                    Server
#   |                         |                         |
#   |------- GET /user/1 ---->|                         |
#   |                         |---- GET /user/1 ------->|
#   |                         |<--- 200 OK + Cache ---- |
#   |<------ 200 OK ----------|                         |
#   |                         | [сохраняет на 300s]     |
#   |                         |                         |
#   |------- GET /user/1 ---->|                         |
#   |<------ 200 OK ----------|                         |
#   |      [из кеша]          |                         |


# @router.post("/")
# def register_user():
#     engine=create_engine(str(settings.SQLALCHEMY_DATABASE_URI))
#     session=sessionmaker(bind=engine)
#     with session() as session:
#         create_UserRepo = UserRepo(session=session).register_user(password, email)
#         return UserResponceModel(**create_UserRepo)
