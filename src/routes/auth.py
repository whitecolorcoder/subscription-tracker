from fastapi import APIRouter, FastAPI, HTTPException, Response 
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr

from src import routes
from src.repository.user import NoUserInDb
from src.routes.deps import JWTServiceDep, PasswordsServiceDep, UserRepoDep

routers= APIRouter(prefix='/auth')

class GetEmailandPassword(BaseModel):
    email: EmailStr 
    password : str
    

@routers.post("/login")
def login(body:GetEmailandPassword, 
          user_repo: UserRepoDep, 
          password_service: PasswordsServiceDep, 
          jwt_services: JWTServiceDep):
    user = user_repo.get_user_by_email(body.email)
    if password_service.create_hash(body.password) == user.hashed_password:
        token = jwt_services.create_jwt(user.id)
        return JSONResponse(status_code=200, content={'token': token})
    else: 
        raise HTTPException(status_code=401, detail="Invalid credentials") 
        

@routers.post("/protected")
def registartion(body:GetEmailandPassword, user_repo: UserRepoDep, password_service: PasswordsServiceDep):
    try:
        user_repo.get_user_by_email(body.email)
        raise HTTPException(
            status_code=400,
                detail="Email already registered")
    except NoUserInDb:
        hashed_password = password_service.create_hash(body.password)
        user_repo.put_user_in_db(email=body.email, hashed_password=hashed_password)
        return Response(status_code=201)

class TokenBodyRequest(BaseModel):
    jwt_token: str
    
@routers.get("/me")
def get_info(body: TokenBodyRequest, jwt_services: JWTServiceDep, user_repo: UserRepoDep):
    user_id = jwt_services.check_jwt(body.jwt_token)
    return user_repo.back_information_from_user(user_id)
    
@routers.delete