from fastapi import APIRouter, FastAPI, Response
from pydantic import BaseModel, EmailStr

from src import routes
from src.routes.deps import PasswordsServiceDep, UserRepoDep

routers= APIRouter(prefix='/auth')

class GetEmailandPassword(BaseModel):
    email: EmailStr 
    password : str
    

# @routes.post("/login")
# def login(body:GetEmailandPassword):
#     if 
    

@routers.post("/protected")
def registartion(body:GetEmailandPassword, user_repo: UserRepoDep, password_service: PasswordsServiceDep):
    hashed_password = password_service.create_hash(body.password)
    user_repo.put_user_in_db(email=body.email, hashed_password=hashed_password)
    return Response(status_code=201)