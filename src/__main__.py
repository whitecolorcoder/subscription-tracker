from src.config import settings
from src.models.base import Base
from sqlalchemy import create_engine
from src.routes.user import router
from src.routes.auth import routers as ouath_router
from fastapi import FastAPI

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI)) #соединение с бд

Base.metadata.create_all(bind=engine) #создание всех таблиц в бд

app = FastAPI() #точка входа приложения
app.include_router(router=router, prefix='/test') 
app.include_router(router=ouath_router)