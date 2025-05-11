
from src.config import settings
from src.models.base import Base
from sqlalchemy import create_engine
from src.routes.user import router
from fastapi import FastAPI
engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))

Base.metadata.create_all(bind=engine)

app = FastAPI() #точка входа приложения
app.include_router(router=router, prefix='/test') 