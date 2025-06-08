from datetime import datetime


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import APIRouter, Path, HTTPException
from src.config import settings
from src.repository.user import NoUserInDb, UserRepo
from pydantic import BaseModel, EmailStr

from .deps import UserRepoDep

router= APIRouter(prefix='/user')

class UserResponceModel(BaseModel):
    id: int 
    email: EmailStr
    hashed_password: str
    is_active: bool
    currency_preference: str
    created_at: datetime

@router.get("/{id}", response_model=UserResponceModel)
def root(id: int, user_repo: UserRepoDep):
    try:
        user = user_repo.back_information_from_user(id)
        return user   
    except NoUserInDb:
        raise HTTPException(status_code=404, detail="User not found")
    
     

    



# @router.post("/")
# def register_user():
#     engine=create_engine(str(settings.SQLALCHEMY_DATABASE_URI))
#     session=sessionmaker(bind=engine)
#     with session() as session: 
#         create_UserRepo = UserRepo(session=session).register_user(password, email)
#         return UserResponceModel(**create_UserRepo)
